"""Local manual UI for simulation. Browser WebGL draws the actual MuJoCo meshes."""
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
        self.config=panda_config()
        self.robot=PandaRobot(self.config)
        self.control=Controller(self.config)
        self.mapping=JointMap.identity(7)
        self.leases=LeaseBook(self.config.lease_s)
        self.lock=threading.RLock()
        self.finished=threading.Event()
        self.seq=0; self.steps=0; self.rx_time=None
        self.start=time.monotonic(); self.error=None
        self.stop_reason="running"
        self.events=[]; self.intervals=[]; self.summary=None
        self.model_json=json.dumps(self.robot.visual_model(),separators=(",",":")).encode()
        self.recorder=Recorder(output,self.config,{"backend":"panda","operator":"browser_joint_sliders",
            "task":"manual_joint_demonstration","transport":"localhost HTTP","time_domain":"robot_monotonic_relative",
            "model_source":"MuJoCo Menagerie franka_emika_panda",
            "model_commit":"4d038b3feae26ec82b46a4d586379114012a8ac7",
            "gripper_semantics":"0=open,1=closed; simulated Panda finger joints"})
        self.thread=threading.Thread(target=self._loop,daemon=True)

    def begin(self):
        self.start=time.monotonic(); self.thread.start()

    def snapshot(self, include_poses=True):
        with self.lock:
            now=time.monotonic()-self.start
            obs=self.robot.read()
            lease=self.leases.issue(now)
            result = {"session":self.leases.session,"lease":lease,"epoch":self.control.epoch,
                "q":obs["q"].tolist(),"target":self.control.goal.tolist(),"gripper":obs["gripper"],
                "mode":self.control.mode,"reason":self.control.reason,"time":now,
                "steps":self.steps,"recorded_rows":self.recorder.rows,"finished":self.finished.is_set(),
                "error":self.error,
                "lower":self.config.lower,"upper":self.config.upper,"summary":self.summary}
            if include_poses:
                result["poses"] = self.robot.visual_poses()
            return result

    def command(self, payload):
        with self.lock:
            if self.finished.is_set():
                raise ValueError("episode has ended")
            now=time.monotonic()-self.start
            expiry=self.leases.check(payload.get("session"),payload.get("lease"),now)
            raw=payload.get("q")
            # Strict wire checks precede mapping, so strings/bools cannot be coerced to angles.
            cmd=Command(self.seq,raw,payload.get("gripper",0),payload.get("deadman",False),payload.get("epoch",""))
            cmd.validate(7)
            cmd.q=self.mapping.apply(raw).tolist()
            self.seq+=1
            ok=self.control.receive(cmd,now,expiry,self.robot.read()["q"])
            if ok and self.control.mode=="ACTIVE": self.rx_time=now
            return {"accepted":ok,"mode":self.control.mode,"reason":self.control.reason}

    def local_action(self, action):
        with self.lock:
            obs=self.robot.read()
            if action=="estop": self.control.stop("ESTOP","local_ui_estop",obs["q"])
            elif action=="reset": self.control.reset_local(obs["q"])
            elif action=="finish": self.stop_reason="operator_saved"; self.finished.set()
            else: raise ValueError("unknown action")

    def _loop(self):
        deadline=time.monotonic(); last=deadline; completed=False
        try:
            while not self.finished.is_set():
                with self.lock:
                    wall=time.monotonic(); now=wall-self.start
                    self.intervals.append(wall-last); last=wall
                    obs=self.robot.read()
                    # Fixed physics step; watchdog uses elapsed wall time. No hardware servo claim.
                    action=self.control.step(now,self.config.dt,obs["q"])
                    if not self.events or self.events[-1]["mode"]!=self.control.mode:
                        self.events.append({"time_s":now,"mode":self.control.mode,"reason":self.control.reason})
                    row=make_row(self.steps,now,obs,self.control,action,self.control.last_seq,self.rx_time)
                    row["simulation_time_s"]=float(self.robot.data.time)
                    self.recorder.append(row)
                    if self.control.mode=="ACTIVE": self.robot.command(action,self.control.gripper,self.config.dt)
                    else: self.robot.stop()
                    self.steps+=1
                deadline+=self.config.dt
                remaining=deadline-time.monotonic()
                if remaining>0: self.finished.wait(remaining)
                else: deadline=time.monotonic()
            completed=True
        except Exception as exc:
            self.error=repr(exc); self.finished.set()
        finally:
            with self.lock: self.robot.close()
            try:
                self.recorder.close(complete=completed)
                if completed: export_npz(self.recorder.path,self.recorder.path/"episode.npz")
            except Exception as exc: self.error=repr(exc)
            elapsed=time.monotonic()-self.start
            self.summary={"backend":"panda","operator":"browser_joint_sliders","steps":self.steps,
                "elapsed_wall_s":elapsed,"actual_hz":self.steps/elapsed,
                "period_p95_ms":float(np.percentile(self.intervals[1:],95))*1000 if len(self.intervals)>1 else None,
                "accepted":self.control.accepted,"rejected":self.control.rejected,
                "events":self.events,"complete":completed and not self.error,"error":self.error,
                "stop_reason":self.stop_reason,"scope":"interactive simulator; no physical robot, force feedback or WAN measurement"}
            (self.recorder.path/"summary.json").write_text(json.dumps(self.summary,indent=2))

    def close(self):
        self.finished.set(); self.thread.join(timeout=10)
        if self.thread.is_alive(): raise RuntimeError("simulation thread did not stop")


def serve_manual(output, port=8080, open_browser=False):
    engine=ManualEngine(output); token=secrets.token_urlsafe(32)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args): pass
        def respond(self,data,ctype="application/json",status=200):
            self.send_response(status); self.send_header("Content-Type",ctype)
            self.send_header("Cache-Control","no-store"); self.send_header("Content-Length",str(len(data)))
            self.end_headers(); self.wfile.write(data)
        def do_GET(self):
            route=self.path.split("?",1)[0]
            if route=="/":
                page=(WEB/"index.html").read_text().replace("__CONTROL_TOKEN__",token)
                self.respond(page.encode(),"text/html; charset=utf-8")
            elif route=="/api/state": self.respond(json.dumps(engine.snapshot()).encode())
            elif route=="/api/control-state": self.respond(json.dumps(engine.snapshot(False)).encode())
            elif route=="/api/model": self.respond(engine.model_json)
            elif route.startswith("/web/"):
                name=route.removeprefix("/web/")
                if name not in {"app.js","control-worker.js","three.module.js","three.core.js","OrbitControls.js"}:
                    self.respond(b"{}",status=404); return
                self.respond((WEB/name).read_bytes(),"text/javascript; charset=utf-8")
            else: self.respond(b"{}",status=404)
        def do_POST(self):
            try:
                if self.headers.get("X-Control-Token")!=token: raise ValueError("invalid local control token")
                size=int(self.headers.get("Content-Length","0"))
                if not 0<size<=16384: raise ValueError("invalid body size")
                payload=json.loads(self.rfile.read(size))
                if self.path=="/api/command": result=engine.command(payload)
                elif self.path=="/api/action": engine.local_action(payload.get("action")); result={"ok":True}
                else: self.respond(b"{}",status=404); return
                self.respond(json.dumps(result).encode())
            except (ValueError,TypeError,KeyError) as exc:
                self.respond(json.dumps({"error":str(exc)}).encode(),status=400)
    server=ThreadingHTTPServer(("127.0.0.1",port),Handler)
    engine.begin()
    url=f"http://127.0.0.1:{server.server_port}"
    print(f"人工控制界面：{url}\n轨迹保存到：{output}\n点击结束保存后可检查数据；Ctrl+C退出服务器。",flush=True)
    if open_browser:
        import webbrowser; webbrowser.open(url)
    try: server.serve_forever(poll_interval=.2)
    except KeyboardInterrupt: pass
    finally: server.server_close(); engine.close()
    return engine.summary
