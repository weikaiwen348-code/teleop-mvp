"""Local-only Panda UI; this is a simulator, never a manufacturer servo."""
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import secrets
import threading
import time
import numpy as np
from .panda import PandaRobot, panda_config
from .control import Controller
from .mapping import JointMap
from .protocol import Command, LeaseBook
from .recording import Recorder, make_row, export_npz

WEB = Path(__file__).parent / "web"


class ManualEngine:
    def __init__(self, output):
        self.config = panda_config()
        self.robot = PandaRobot(self.config)
        self.control = Controller(self.config)
        self.mapping = JointMap.identity(7)
        self.leases = LeaseBook(self.config.lease_s)
        self.lock = threading.RLock()
        self.finished = threading.Event()
        self.finalized = threading.Event()
        self.seq = self.steps = 0
        self.rx_time = None
        self.owner = None
        self.input_seq = -1
        self.start = time.monotonic()
        self.error = None
        self.stop_reason = "running"
        self.events, self.intervals = [], []
        self.summary = None
        try:
            self.model_json = json.dumps(self.robot.visual_model(), separators=(",", ":")).encode()
            self.recorder = Recorder(output, self.config, {
                "backend": "panda", "operator": "browser_joint_sliders",
                "operator_execution": "browser_input_not_independently_verified",
                "human_collected": None, "task": "manual_joint_demonstration",
                "transport": "localhost HTTP", "time_domain": "robot_monotonic_relative",
                "model_source": "MuJoCo Menagerie franka_emika_panda",
                "model_commit": "4d038b3feae26ec82b46a4d586379114012a8ac7",
                "gripper_semantics": "0=open,1=closed; simulated Panda finger joints"})
        except BaseException:
            self.robot.close()
            raise
        self.thread = threading.Thread(target=self._loop, daemon=True)

    def begin(self):
        self.start = time.monotonic()
        self.thread.start()

    def snapshot(self, include_poses=True):
        with self.lock:
            now = time.monotonic() - self.start
            obs = self.robot.read()
            result = {"session": self.leases.session, "lease": self.leases.issue(now),
                "epoch": self.control.epoch, "q": obs["q"].tolist(),
                "target": self.control.goal.tolist(), "gripper": obs["gripper"],
                "mode": self.control.mode, "reason": self.control.reason, "time": now,
                "steps": self.steps, "recorded_rows": self.recorder.rows,
                "finished": self.finished.is_set(), "finalized": self.finalized.is_set(),
                "error": self.error, "lower": self.config.lower, "upper": self.config.upper,
                "summary": self.summary, "output": str(self.recorder.path.resolve())}
            if include_poses:
                result["poses"] = self.robot.visual_poses()
            return result

    def command(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("command must be a JSON object")
        with self.lock:
            if self.finished.is_set():
                raise ValueError("episode has ended")
            now = time.monotonic() - self.start
            expiry = self.leases.check(payload.get("session"), payload.get("lease"), now)
            cmd = Command(self.seq, payload.get("q"), payload.get("gripper", 0),
                          payload.get("deadman", False), payload.get("epoch", ""))
            cmd.validate(7)
            client = payload.get("client_id")
            seq = payload.get("input_seq")
            if not isinstance(client, str) or not 1 <= len(client) <= 64:
                raise ValueError("invalid browser client id")
            if type(seq) is not int or not 0 <= seq < 2**53:
                raise ValueError("invalid browser input sequence")
            if self.owner is not None and self.owner != client:
                raise ValueError("另一页面正在控制；请关闭旧页面并点击本地复位")
            if self.owner == client and seq <= self.input_seq:
                raise ValueError("replayed or out-of-order browser command")
            cmd.q = self.mapping.apply(cmd.q).tolist()
            self.seq += 1
            ok = self.control.receive(cmd, now, expiry, self.robot.read()["q"])
            if self.owner == client:
                self.input_seq = seq
            if ok and self.control.mode == "ACTIVE":
                self.owner, self.input_seq, self.rx_time = client, seq, now
            return {"accepted": ok, "mode": self.control.mode, "reason": self.control.reason}

    def local_action(self, action):
        with self.lock:
            if self.finished.is_set():
                if action == "finish":
                    return
                raise ValueError("episode has ended")
            obs = self.robot.read()
            if action == "estop":
                self.control.stop("ESTOP", "local_ui_estop", obs["q"])
            elif action == "reset":
                self.control.reset_local(obs["q"])
                self.owner, self.input_seq = None, -1
            elif action == "finish":
                self.stop_reason = "operator_saved"
                self.finished.set()
            else:
                raise ValueError("unknown action")

    def _loop(self):
        deadline = last = time.monotonic()
        completed = exported = False
        try:
            while not self.finished.is_set():
                with self.lock:
                    wall = time.monotonic()
                    now, wall_dt = wall - self.start, wall - last
                    self.intervals.append(wall_dt)
                    last = wall
                    obs = self.robot.read()
                    # The physical integration step stays fixed; the scheduling
                    # deadline is checked independently using elapsed wall time.
                    if self.steps and wall_dt > 2.5 * self.config.dt and self.control.mode == "ACTIVE":
                        self.control.stop("FAULT", "control_deadline", obs["q"])
                    action = self.control.step(now, self.config.dt, obs["q"])
                    if not self.events or self.events[-1]["mode"] != self.control.mode:
                        self.events.append({"time_s": now, "mode": self.control.mode, "reason": self.control.reason})
                    row = make_row(self.steps, now, obs, self.control, action, self.control.last_seq, self.rx_time)
                    row["simulation_time_s"] = float(self.robot.data.time)
                    self.recorder.append(row)
                    if self.control.mode == "ACTIVE":
                        self.robot.command(action, self.control.gripper, self.config.dt)
                    else:
                        self.robot.stop()
                    self.steps += 1
                deadline += self.config.dt
                remaining = deadline - time.monotonic()
                if remaining > 0:
                    self.finished.wait(remaining)
                else:
                    deadline = time.monotonic()
            completed = True
        except Exception as exc:
            self.error = repr(exc)
            self.stop_reason = "runtime_error"
            self.finished.set()
        finally:
            try:
                with self.lock:
                    self.robot.close()
            except Exception as exc:
                self.error = self.error or repr(exc)
                completed = False
            try:
                self.recorder.close(complete=completed)
                if completed:
                    export_npz(self.recorder.path, self.recorder.path / "episode.npz")
                    exported = True
            except Exception as exc:
                self.error = self.error or repr(exc)
            elapsed = time.monotonic() - self.start
            self.summary = {"backend": "panda", "operator": "browser_joint_sliders",
                "steps": self.steps, "elapsed_wall_s": elapsed, "actual_hz": self.steps / max(elapsed, 1e-9),
                "period_p95_ms": float(np.percentile(self.intervals[1:], 95)) * 1000 if len(self.intervals) > 1 else None,
                "accepted": self.control.accepted, "rejected": self.control.rejected, "events": self.events,
                "recording_complete": self.recorder.meta.get("complete") is True,
                "export_complete": exported, "complete": completed and exported and not self.error,
                "error": self.error, "stop_reason": self.stop_reason,
                "scope": "interactive simulator; no physical robot, force feedback or WAN measurement"}
            try:
                (self.recorder.path / "summary.json").write_text(json.dumps(self.summary, indent=2), encoding="utf-8")
            except Exception as exc:
                self.error = self.error or repr(exc)
                self.summary.update(complete=False, error=self.error)
            finally:
                self.finalized.set()

    def close(self):
        if self.stop_reason == "running":
            self.stop_reason = "server_interrupted"
        self.finished.set()
        if self.thread.ident is not None:
            self.thread.join(timeout=10)
            if self.thread.is_alive():
                raise RuntimeError("simulation thread did not stop")
        else:
            try:
                self.robot.close()
            finally:
                self.recorder.close(complete=False)
                self.finalized.set()


def create_manual_server(output, port=8080):
    """Bind before allocating physics/recorder; a busy port leaves no episode."""
    token = secrets.token_urlsafe(32)
    engine = None

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(3)

        def log_message(self, *args):
            pass

        def respond(self, data, ctype="application/json", status=200):
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            try:
                self.wfile.write(data)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def do_GET(self):
            route = self.path.split("?", 1)[0]
            if route == "/":
                page = (WEB / "index.html").read_text(encoding="utf-8").replace("__CONTROL_TOKEN__", token)
                self.respond(page.encode(), "text/html; charset=utf-8")
            elif route in ("/api/state", "/api/control-state"):
                self.respond(json.dumps(engine.snapshot(route == "/api/state")).encode())
            elif route == "/api/model":
                self.respond(engine.model_json)
            elif route == "/api/summary":
                self.respond(json.dumps(engine.summary).encode())
            elif route.startswith("/web/") and route[5:] in {
                    "app.js", "control-worker.js", "three.module.js", "three.core.js", "OrbitControls.js"}:
                self.respond((WEB / route[5:]).read_bytes(), "text/javascript; charset=utf-8")
            else:
                self.respond(b"{}", status=404)

        def do_POST(self):
            try:
                if self.headers.get("X-Control-Token") != token:
                    raise ValueError("invalid local control token")
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 16384:
                    raise ValueError("invalid body size")
                payload = json.loads(self.rfile.read(size))
                if not isinstance(payload, dict):
                    raise ValueError("request must be a JSON object")
                if self.path == "/api/command":
                    result = engine.command(payload)
                elif self.path == "/api/action":
                    engine.local_action(payload.get("action"))
                    result = {"ok": True}
                else:
                    self.respond(b"{}", status=404)
                    return
                self.respond(json.dumps(result).encode())
            except (ValueError, TypeError, KeyError, TimeoutError) as exc:
                self.respond(json.dumps({"error": str(exc)}).encode(), status=400)

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    try:
        engine = ManualEngine(output)
        engine.begin()
    except BaseException:
        server.server_close()
        if engine is not None:
            engine.close()
        raise
    return server, engine


def serve_manual(output, port=8080, open_browser=False, auto_exit=False):
    server, engine = create_manual_server(output, port)
    url = f"http://127.0.0.1:{server.server_port}"
    ending = "保存完成后会自动退出并生成报告。" if auto_exit else "Ctrl+C退出服务器。"
    print(f"人工控制界面：{url}\n轨迹保存到：{Path(output).resolve()}\n点击结束保存后可检查数据；{ending}", flush=True)
    try:
        if open_browser:
            import webbrowser
            webbrowser.open(url)
        if auto_exit:
            def close_when_saved():
                engine.finalized.wait()
                # Allow the page to fetch and display the final save result.
                threading.Event().wait(2)
                server.shutdown()
            threading.Thread(target=close_when_saved, daemon=True).start()
        server.serve_forever(poll_interval=.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        engine.close()
    return engine.summary
