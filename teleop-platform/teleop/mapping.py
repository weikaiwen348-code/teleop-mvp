"""Homomorphic mapping in radians. Different topologies require a separate IK layer."""
from dataclasses import dataclass
import numpy as np
from .config import vector


@dataclass
class JointMap:
    signs: list
    offsets: list
    gains: list
    reference: list

    def __post_init__(self):
        self.n = len(self.signs)
        for key in ("signs", "offsets", "gains", "reference"):
            setattr(self, key, vector(getattr(self, key), self.n, key))
        if not np.isin(self.signs, [-1, 1]).all() or np.any(self.gains <= 0):
            raise ValueError("signs must be +/-1 and gains must be positive")

    def apply(self, leader):
        q = vector(leader, self.n, "leader")
        return self.reference + self.signs * self.gains * (q - self.offsets)

    @classmethod
    def identity(cls, n):
        return cls([1] * n, [0] * n, [1] * n, [0] * n)


def fit_calibration(leader, follower):
    """Fit q_f = slope*q_l + intercept per joint from paired stationary poses.

    No angle unwrapping is guessed. Supply continuous radians with correct joint order.
    Residuals on calibration poses are NOT independent accuracy validation.
    """
    x, y = np.asarray(leader, float), np.asarray(follower, float)
    if x.ndim != 2 or x.shape != y.shape or x.shape[0] < 3:
        raise ValueError("at least three matched poses and equal DOFs required")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("nonfinite calibration samples")
    if np.any(np.ptp(x, axis=0) < 0.15):
        raise ValueError("insufficient joint excitation: need >=0.15 rad per joint")
    slopes, offsets, rms = [], [], []
    for j in range(x.shape[1]):
        slope, intercept = np.linalg.lstsq(np.c_[x[:, j], np.ones(len(x))], y[:, j], rcond=None)[0]
        if not 0.1 <= abs(slope) <= 10:
            raise ValueError("implausible scale: check units, ordering and topology")
        slopes.append(float(slope))
        offsets.append(float(-intercept / slope))
        rms.append(float(np.sqrt(np.mean((y[:, j] - slope*x[:, j] - intercept)**2))))
    return {"signs": np.sign(slopes).astype(int).tolist(), "offsets": offsets,
            "gains": np.abs(slopes).tolist(), "reference": [0.0]*x.shape[1]}, rms
