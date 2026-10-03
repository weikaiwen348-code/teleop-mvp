import heapq
import time
from pathlib import Path
import json
import numpy as np
from .control import Controller
from .protocol import Command, LeaseBook
from .robot import make_robot
from .recording import Recorder, make_row


def leader_signal(t, home):
    # Continuous startup at home; intentionally slow low-amplitude joint motion.
    return np.array(home) + 0.12*np.sin(0.7*t)*np.linspace(0.5, 1.0, len(home))


def run_sim(config, output, duration=6, delay_ms=5, jitter_ms=1, loss=0,
            blackout_at=None, seed=7, backend="toy", realtime=False, viewer=False):
    if not np.isfinite([duration, delay_ms, jitter_ms, loss]).all() or duration <= 0 or min(delay_ms, jitter_ms) < 0 or not 0 <= loss < 1:
        raise ValueError("invalid simulation parameters")
    if blackout_at is not None and not 0 < blackout_at < duration:
        raise ValueError("blackout must be inside duration")
    if viewer and not realtime:
        raise ValueError("viewer requires realtime pacing")
    robot, controller = make_robot(config, backend, viewer), Controller(config)
    leases = LeaseBook(config.lease_s)
    rng = np.random.default_rng(seed)
    recorder = Recorder(output, config, {"backend": backend, "task": "synthetic_joint_tracking",
        "operator": "virtual_gello", "seed": seed, "network": {"one_way_delay_ms": delay_ms,
        "jitter_std_ms": jitter_ms, "independent_loss_each_direction": loss},
        "blackout_at_sim_s": blackout_at, "time_domain": "simulation_clock", "real_time_pacing": realtime})
    events = []
    uid, seq = 0, 0
    arm_epoch = None
    rx_time, source_time = None, None
    accepted_age, loop_cost, goal_error, track_error, applied_error = [], [], [], [], []
    first_hold = None
    active_steps = 0
    previous_action = None
    wall_start = time.perf_counter()

    def enqueue(now, kind, data):
        nonlocal uid
        if rng.random() < loss:
            return
        delay = max(0, rng.normal(delay_ms, jitter_ms))/1000
        uid += 1
        heapq.heappush(events, (now+delay, uid, kind, data))

    completed = False
    try:
        for i in range(int(np.ceil(duration/config.dt))):
            t = i*config.dt
            begin = time.perf_counter()
            obs = robot.read()
            lease = leases.issue(t)
            enqueue(t, "state", {"lease": lease, "epoch": controller.epoch})
            # Timestamps are quantized to control ticks; metrics state this explicitly.
            while events and events[0][0] <= t+1e-12:
                _, _, kind, data = heapq.heappop(events)
                if kind == "state":
                    if blackout_at is not None and t >= blackout_at:
                        continue
                    if arm_epoch is None:
                        arm_epoch = data["epoch"]  # Never automatically rearm after a stop.
                    cmd = Command(seq, leader_signal(t, config.home).tolist(), float(0.25*(1-np.cos(t))), True, arm_epoch)
                    seq += 1
                    enqueue(t, "command", (cmd, data["lease"], t))
                else:
                    cmd, token, sampled = data
                    try:
                        expiry = leases.check(leases.session, token, t)
                    except ValueError:
                        controller.rejected += 1
                        continue
                    if controller.receive(cmd, t, expiry, obs["q"]) and controller.mode == "ACTIVE":
                        rx_time, source_time = t, sampled
                        accepted_age.append((t-sampled)*1000)
            action = controller.step(t, config.dt, obs["q"])
            if controller.mode == "ACTIVE":
                active_steps += 1
                goal_error.extend((obs["q"]-controller.goal).tolist())
                track_error.extend((obs["q"]-action).tolist())
                if previous_action is not None:
                    applied_error.extend((obs["q"]-previous_action).tolist())
            if blackout_at is not None and t >= blackout_at and first_hold is None and controller.reason == "input_timeout":
                first_hold = t
            recorder.append(make_row(i, t, obs, controller, action, controller.last_seq, rx_time, source_time), offline_wait=not realtime)
            if controller.mode == "ACTIVE":
                robot.command(action, controller.gripper, config.dt)
            else:
                robot.stop()
            previous_action = action.copy()
            loop_cost.append((time.perf_counter()-begin)*1000)
            if realtime:
                time.sleep(max(0, wall_start+(i+1)*config.dt-time.perf_counter()))
        completed = True
    finally:
        robot.close()
        recorder.close(complete=completed)
    def rms(x):
        return float(np.sqrt(np.mean(np.square(x)))) if x else None
    summary = {"backend": backend, "duration_sim_s": duration, "wall_s": time.perf_counter()-wall_start,
               "simulation_hz": config.hz, "steps": recorder.rows, "active_steps": active_steps,
               "commands_accepted": controller.accepted, "commands_rejected": controller.rejected,
               "accepted_sample_to_receive_p95_ms": float(np.percentile(accepted_age,95)) if accepted_age else None,
               "compute_per_tick_p95_ms": float(np.percentile(loop_cost,95)),
               "raw_target_vs_observation_rmse_rad": rms(goal_error),
               "next_action_vs_observation_rmse_rad": rms(track_error),
               "previous_action_vs_observation_rmse_rad": rms(applied_error),
               "blackout_to_hold_ms": None if first_hold is None else (first_hold-blackout_at)*1000,
               "final_mode": controller.mode, "final_reason": controller.reason,
               "measurement_scope": "synthetic input; discrete network simulator; latency quantized to control ticks; no real network/hardware claim"}
    Path(output, "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
