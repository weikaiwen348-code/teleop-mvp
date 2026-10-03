"""Two-process UDP reference. Simulation backends only; authenticated, not encrypted."""
from dataclasses import asdict
from pathlib import Path
import json
import socket
import threading
import time
import queue
import numpy as np
from .control import Controller
from .mapping import JointMap
from .protocol import Command, LeaseBook, encode, decode, MAX_PACKET
from .recording import Recorder, make_row
from .robot import make_robot
from .simulation import leader_signal


def read_key(path):
    key = Path(path).read_bytes()
    if len(key) < 32:
        raise ValueError("key must contain >=32 random bytes; use keygen")
    return key


def serve(config, output, keyfile, host="127.0.0.1", port=8765, duration=30, backend="toy"):
    if not np.isfinite(duration) or duration <= 0:
        raise ValueError("duration must be positive")
    key = read_key(keyfile)
    robot = make_robot(config, backend)
    control, leases = Controller(config), LeaseBook(config.lease_s)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.setblocking(False)
    log = Recorder(output, config, {"backend": backend, "transport": "UDP-HMAC-SHA256",
        "task": "remote_joint_tracking", "operator": "remote_client", "time_domain": "robot_monotonic_relative"})
    start = time.monotonic()
    last = start
    next_tick = start
    peer = None
    rx_time = None
    bad_packets = 0
    overruns = 0
    tick = 0
    completed = False
    intervals = []
    try:
        while time.monotonic()-start < duration:
            now_abs = time.monotonic()
            now = now_abs-start
            dt = config.dt if tick == 0 else now_abs-last
            last = now_abs
            intervals.append(dt)
            obs = robot.read()
            for _ in range(64):  # Bounded work: watchdog runs even during an input flood.
                try:
                    wire, addr = sock.recvfrom(MAX_PACKET+1)
                except BlockingIOError:
                    break
                try:
                    msg = decode(wire, key)
                    if msg.get("kind") == "hello":
                        if peer is None:
                            peer = addr
                        continue
                    if addr != peer or msg.get("kind") != "command":
                        raise ValueError("wrong peer/type")
                    expiry = leases.check(msg.get("session"), msg.get("lease"), now)
                    cmd = Command(**msg["command"])
                    if control.receive(cmd, now, expiry, obs["q"]) and control.mode == "ACTIVE":
                        rx_time = now
                except (ValueError, TypeError, KeyError):
                    bad_packets += 1
            action = control.step(now, dt, obs["q"])
            log.append(make_row(tick, now, obs, control, action, control.last_seq, rx_time))
            if control.mode == "ACTIVE":
                robot.command(action, control.gripper, dt)
            else:
                robot.stop()
            if peer:
                state = {"v": 1, "kind": "state", "session": leases.session,
                    "lease": leases.issue(now), "state_seq": tick, "q": robot.read()["q"].tolist(),
                    "mode": control.mode, "reason": control.reason, "epoch": control.epoch,
                    "n": config.n, "config_sha256": config.digest(), "robot_time_s": now,
                    "accepted_seq": control.last_seq}
                try:
                    sock.sendto(encode(state, key), peer)
                except BlockingIOError:
                    bad_packets += 1
            tick += 1
            next_tick += config.dt
            remaining = next_tick-time.monotonic()
            if remaining < 0:
                overruns += 1
                next_tick = time.monotonic()  # Skip missed ticks; never burst old trajectories.
            else:
                time.sleep(remaining)
        completed = True
    except KeyboardInterrupt:
        completed = True
    finally:
        robot.close()
        sock.close()
        log.close(complete=completed)
    result = {"backend": backend, "elapsed_wall_s": time.monotonic()-start, "steps": tick,
        "actual_hz": tick/(time.monotonic()-start), "period_p95_ms": float(np.percentile(intervals,95))*1000,
        "overruns": overruns, "bad_packets": bad_packets, "accepted": control.accepted,
        "rejected": control.rejected, "final_mode": control.mode, "final_reason": control.reason,
        "measurement_scope": "local wall-clock process run; no one-way latency measurement"}
    Path(output,"summary.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    return result


class GelloInput:
    """Optional upstream GELLO input, unverified on hardware.

    Upstream already applies joint signs/offsets. Do not apply them twice.
    Serial reading belongs in a separate input process before real robot deployment.
    """
    def __init__(self, filename, n):
        from gello.agents.gello_agent import GelloAgent, DynamixelRobotConfig
        cfg = json.loads(Path(filename).read_text())
        if any(v is None for v in cfg["joint_offsets"]) or any(v is None for v in cfg["gripper_config"]):
            raise ValueError("fill measured GELLO joint offsets and gripper endpoints first")
        if len(cfg["joint_ids"]) != n:
            raise ValueError("GELLO topology does not match target DOF")
        self.agent = GelloAgent(port=cfg["port"], dynamixel_config=DynamixelRobotConfig(
            joint_ids=cfg["joint_ids"], joint_offsets=cfg["joint_offsets"],
            joint_signs=cfg["joint_signs"], gripper_config=tuple(cfg["gripper_config"])))
        self.n = n
        self.invert = bool(cfg.get("invert_gripper", False))

    def read(self, t):
        a = np.asarray(self.agent.act({}), float)
        if a.shape != (self.n+1,) or not np.isfinite(a).all():
            raise ValueError("unexpected GELLO state")
        g = 1-float(a[-1]) if self.invert else float(a[-1])
        if not 0 <= g <= 1:
            raise ValueError("calibrate GELLO gripper range")
        return a[:-1], g


def client(config, keyfile, host="127.0.0.1", port=8765, duration=20, virtual=False,
           gello_config=None, calibration=None):
    if not np.isfinite(duration) or duration <= 0:
        raise ValueError("duration must be positive")
    key = read_key(keyfile)
    # Connected UDP validates source endpoint for state traffic.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((host, port))
    sock.settimeout(0.05)
    mapping = JointMap(**json.loads(Path(calibration).read_text())) if calibration else JointMap.identity(config.n)
    if mapping.n != config.n:
        raise ValueError("calibration DOF mismatch")
    source = GelloInput(gello_config, config.n) if gello_config else None
    if source and virtual:
        raise ValueError("virtual and GELLO source are exclusive")
    inputs = queue.Queue()
    if not virtual:
        print("模拟后端交互：a+回车使能，h+回车保持，e+回车急停，q+回车退出。终端开关不是实体使能开关。", flush=True)
        def input_loop():
            while True:
                try:
                    inputs.put(input().strip().lower())
                except EOFError:
                    inputs.put("q")
                    return
        threading.Thread(target=input_loop, daemon=True).start()
    start = time.monotonic()
    last_hello = -1.0
    seq, state_seq = 0, -1
    session = None
    arm_epoch = ""
    deadman, stop = False, False
    virtual_armed = False
    virtual_signal_start = None
    sent_at = {}
    ack_ms = []
    try:
        while time.monotonic()-start < duration:
            elapsed = time.monotonic()-start
            if elapsed-last_hello > 0.5:
                sock.send(encode({"v":1,"kind":"hello"},key))
                last_hello = elapsed
            try:
                state = decode(sock.recv(MAX_PACKET+1), key)
            except (socket.timeout, ConnectionRefusedError):
                continue
            except ValueError:
                continue
            if state.get("kind") != "state" or state.get("config_sha256") != config.digest():
                raise ValueError("state/config mismatch")
            if session is None:
                session = state["session"]
            elif state["session"] != session:
                raise RuntimeError("server restarted: restart client and explicitly rearm")
            if state["state_seq"] <= state_seq:
                continue
            state_seq = state["state_seq"]
            acknowledged = state.get("accepted_seq", -1)
            if acknowledged in sent_at:
                ack_ms.append((time.monotonic()-sent_at[acknowledged])*1000)
            sent_at = {k:v for k,v in sent_at.items() if k > acknowledged and time.monotonic()-v < 2}
            if virtual and not virtual_armed:
                deadman, arm_epoch, virtual_armed = True, state["epoch"], True
                # Start the synthetic motion at home only after the backend is ready.
                # Heavy model loading must not advance the source beyond arm alignment.
                virtual_signal_start = time.monotonic()-start
            while not inputs.empty():
                keypress = inputs.get_nowait()
                if keypress == "q":
                    return {"sent": seq, "reason": "operator_exit"}
                if keypress == "a":
                    deadman, arm_epoch = True, state["epoch"]
                elif keypress == "h":
                    deadman = False
                elif keypress == "e":
                    stop = True
            # Fresh leader sample is taken only AFTER receiving a new robot challenge.
            sampled_now = time.monotonic()-start
            signal_t = sampled_now-virtual_signal_start if virtual_signal_start is not None else sampled_now
            q, g = source.read(sampled_now) if source else (leader_signal(signal_t, config.home), 0.0)
            mapped = mapping.apply(q)
            cmd = Command(seq, mapped.tolist(), g, deadman, arm_epoch, stop).validate(config.n)
            envelope = {"v":1,"kind":"command","session":session,"lease":state["lease"],"command":asdict(cmd)}
            sock.send(encode(envelope,key))
            sent_at[seq] = time.monotonic()
            seq += 1
    finally:
        # Even if final datagram is lost or serial read stalls, server lease expiration stops.
        sock.close()
    return {"sent":seq,"ack_p95_ms":float(np.percentile(ack_ms,95)) if ack_ms else None,
            "ack_metric":"command send to state acknowledging receipt; includes server cycle; not one-way latency"}
