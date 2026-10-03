from dataclasses import dataclass, asdict
import hashlib
import json
import numpy as np


def vector(value, n, name):
    a = np.asarray(value, dtype=float)
    if a.shape != (n,) or not np.isfinite(a).all():
        raise ValueError(f"{name}: expected {n} finite numbers")
    return a


@dataclass
class Config:
    name: str
    home: list
    lower: list
    upper: list
    velocity: list
    acceleration: list
    hz: float = 100.0
    watchdog_s: float = 0.15
    lease_s: float = 0.12
    align_tolerance_rad: float = 0.08
    tracking_fault_rad: float = 0.35

    @property
    def n(self):
        return len(self.home)

    @property
    def dt(self):
        return 1.0 / self.hz

    def validate(self):
        if not 1 <= self.n <= 16:
            raise ValueError("invalid degrees of freedom")
        for name in ("home", "lower", "upper", "velocity", "acceleration"):
            vector(getattr(self, name), self.n, name)
        for name in ("hz", "watchdog_s", "lease_s", "align_tolerance_rad", "tracking_fault_rad"):
            x = getattr(self, name)
            if not np.isfinite(x) or x <= 0:
                raise ValueError(f"invalid {name}")
        if not 10 <= self.hz <= 500 or not self.dt < self.lease_s <= self.watchdog_s <= 1:
            raise ValueError("invalid timing configuration")
        lo, hi, q = map(np.array, (self.lower, self.upper, self.home))
        if np.any(lo >= hi) or np.any(q <= lo) or np.any(q >= hi):
            raise ValueError("home must be strictly inside joint limits")
        if np.any(np.array(self.velocity) <= 0) or np.any(np.array(self.acceleration) <= 0):
            raise ValueError("motion limits must be positive")
        return self

    def digest(self):
        return hashlib.sha256(json.dumps(asdict(self), sort_keys=True).encode()).hexdigest()


def load_config(path=None):
    if path:
        with open(path, encoding="utf-8") as f:
            return Config(**json.load(f)).validate()
    return Config("panda7_layout_sim_only", [0, -0.4, 0, -1.8, 0, 1.4, 0.7],
                  [-2.5, -1.5, -2.5, -2.8, -2.5, 0.1, -2.5],
                  [2.5, 1.5, 2.5, -0.2, 2.5, 3.4, 2.5],
                  [0.4] * 7, [1.0] * 7).validate()
