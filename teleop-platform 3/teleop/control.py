"""Supervisory simulation controller; never use as a certified hardware safety layer."""
import secrets
import numpy as np
from .config import vector


class Controller:
    def __init__(self, config):
        self.c = config.validate()
        self.mode = "DISARMED"
        self.reason = "startup"
        self.epoch = secrets.token_hex(12)
        self.q = np.array(config.home, float)
        self.v = np.zeros(config.n)
        self.goal = self.q.copy()
        self.gripper = 0.0
        self.last_seq = -1
        self.last_rx = None
        self.expires = -1.0
        self.accepted = 0
        self.rejected = 0

    def stop(self, mode, reason, observed):
        if self.mode != mode or self.reason != reason:
            self.epoch = secrets.token_hex(12)
        self.mode, self.reason = mode, reason
        self.q = vector(observed, self.c.n, "observed").copy()
        self.goal = self.q.copy()
        # Immediate zero is a toy-simulator stop. Hardware needs a local brake trajectory.
        self.v[:] = 0

    def reset_local(self, observed):
        """Explicit local acknowledgement only; no network command calls this."""
        self.stop("DISARMED", "local_reset", observed)

    def receive(self, cmd, now, expires, observed):
        try:
            cmd.validate(self.c.n)
            obs = vector(observed, self.c.n, "observed")
        except ValueError:
            self.rejected += 1
            return False
        if cmd.seq <= self.last_seq or not np.isfinite(now) or not np.isfinite(expires) or expires <= now:
            self.rejected += 1
            return False
        if cmd.estop:
            self.last_seq = cmd.seq
            self.stop("ESTOP", "remote_estop", obs)
            return True
        if self.mode in ("ESTOP", "FAULT"):
            self.rejected += 1
            return False
        if not cmd.deadman:
            self.last_seq = cmd.seq
            self.stop("HOLD", "deadman_released", obs)
            return True
        # Every moving command must belong to the current enable generation,
        # including while already ACTIVE after a local reset/rearm.
        if cmd.arm_epoch != self.epoch:
            self.rejected += 1
            return False
        target = np.asarray(cmd.q)
        if np.any(target < self.c.lower) or np.any(target > self.c.upper):
            self.rejected += 1
            return False
        self.last_seq = cmd.seq
        if self.mode != "ACTIVE":
            if np.max(np.abs(target-obs)) > self.c.align_tolerance_rad:
                self.rejected += 1
                return False
            self.q, self.v = obs.copy(), np.zeros(self.c.n)
            self.mode, self.reason = "ACTIVE", "armed"
        self.goal = target.copy()
        self.gripper = float(cmd.gripper)
        self.last_rx, self.expires = now, expires
        self.accepted += 1
        return True

    def step(self, now, dt, observed):
        obs = vector(observed, self.c.n, "observed")
        if not np.isfinite(now) or not np.isfinite(dt) or dt <= 0:
            raise ValueError("time must be finite and dt must be positive")
        if self.mode != "ACTIVE":
            return self.q.copy()
        if now >= self.expires or self.last_rx is None or now-self.last_rx >= self.c.watchdog_s:
            self.stop("HOLD", "input_timeout", obs)
            return self.q.copy()
        if dt > 2.5*self.c.dt:
            self.stop("FAULT", "control_deadline", obs)
            return self.q.copy()
        if np.max(np.abs(obs-self.q)) > self.c.tracking_fault_rad:
            self.stop("FAULT", "tracking_error", obs)
            return self.q.copy()
        a, vmax = np.array(self.c.acceleration), np.array(self.c.velocity)
        # Discrete conservative braking envelope for v_next and remaining joint travel.
        room_up = np.maximum(np.array(self.c.upper)-self.q, 0)
        room_dn = np.maximum(self.q-np.array(self.c.lower), 0)
        up = np.minimum(vmax, np.sqrt((a*dt)**2+2*a*room_up)-a*dt)
        dn = np.minimum(vmax, np.sqrt((a*dt)**2+2*a*room_dn)-a*dt)
        # Brake toward the target as well as toward physical joint boundaries.
        # A target jump behind a moving reference still obeys the acceleration limit.
        delta = self.goal-self.q
        goal_speed = np.sqrt((a*dt)**2+2*a*np.abs(delta))-a*dt
        wanted = np.clip(np.sign(delta)*goal_speed, -dn, up)
        self.v += np.clip(wanted-self.v, -a*dt, a*dt)
        self.q += self.v*dt
        # A violated braking invariant is a fault, not silent clamping.
        if np.any(self.q < np.array(self.c.lower)-1e-9) or np.any(self.q > np.array(self.c.upper)+1e-9):
            self.stop("FAULT", "joint_limit", obs)
        return self.q.copy()
