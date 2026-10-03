"""Append-only, bounded asynchronous recording; incomplete episodes stay visible."""
from pathlib import Path
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
import queue
import threading
import numpy as np


class Recorder:
    def __init__(self, directory, config, metadata=None, queue_size=2048):
        self.path = Path(directory)
        self.path.mkdir(parents=True, exist_ok=False)
        self.meta = {"schema_version": "teleop-1.0", "created_utc": datetime.now(timezone.utc).isoformat(),
                     "config": asdict(config), "config_sha256": config.digest(), "joint_unit": "rad",
                     "time_unit": "s", "time_domain": "robot_local_monotonic",
                     "action_semantics": "safe absolute joint position command applied AFTER observation",
                     "gripper_semantics": "normalized: 0=open, 1=closed; sim scalar, no physical gripper",
                     "success": None, "success_source": "unlabeled", "complete": False}
        self.meta.update(metadata or {})
        self._write_meta()
        self.rows = 0
        self.failure = None
        self.queue = queue.Queue(maxsize=queue_size)
        self.worker = threading.Thread(target=self._run, daemon=True)
        self.worker.start()

    def _write_meta(self):
        temp = self.path / "metadata.json.tmp"
        temp.write_text(json.dumps(self.meta, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
        temp.replace(self.path / "metadata.json")

    def _run(self):
        try:
            with (self.path / "steps.jsonl").open("x", encoding="utf-8") as f:
                while True:
                    item = self.queue.get()
                    if item is None:
                        break
                    f.write(item + "\n")
                    self.rows += 1
                    if self.rows % 100 == 0:
                        f.flush()
        except Exception as exc:
            self.failure = repr(exc)

    def append(self, row, offline_wait=False):
        if self.failure:
            raise RuntimeError(f"recorder failed: {self.failure}")
        data = json.dumps(row, separators=(",", ":"), allow_nan=False)
        try:
            if offline_wait:
                # Accelerated offline simulation may outpace disk; live control never waits here.
                self.queue.put(data, timeout=5)
            else:
                self.queue.put_nowait(data)
        except queue.Full as exc:
            self.failure = "recorder queue overflow; no silent sample drops"
            raise RuntimeError(self.failure) from exc

    def close(self, complete=True):
        if self.worker.is_alive():
            try:
                self.queue.put(None, timeout=2)
            except queue.Full:
                self.failure = "writer unresponsive"
            self.worker.join(timeout=5)
        if self.worker.is_alive():
            self.failure = "writer did not stop"
        self.meta.update(complete=bool(complete and not self.failure), rows=self.rows,
                         writer_error=self.failure)
        if not self.worker.is_alive() and (self.path / "steps.jsonl").exists():
            self.meta["steps_sha256"] = hashlib.sha256((self.path / "steps.jsonl").read_bytes()).hexdigest()
        self._write_meta()
        if self.failure:
            raise RuntimeError(self.failure)


def make_row(index, t, observed, control, action, source_seq, rx_time, source_time=None):
    return {"step": index, "t_robot_s": float(t), "observation.q": observed["q"].tolist(),
            "observation.dq": observed["dq"].tolist(), "observation.gripper": observed["gripper"],
            "action.q": action.tolist(), "action.gripper": control.gripper,
            "target.q": control.goal.tolist(), "mode": control.mode, "event": control.reason,
            "source_seq": int(source_seq), "rx_robot_s": rx_time,
            "source_sim_s": source_time, "sample_weight": 1 if control.mode == "ACTIVE" else 0}


def read_episode(path):
    path = Path(path)
    meta = json.loads((path / "metadata.json").read_text())
    if not meta.get("complete"):
        raise ValueError("episode is incomplete")
    raw = (path / "steps.jsonl").read_bytes()
    if hashlib.sha256(raw).hexdigest() != meta.get("steps_sha256"):
        raise ValueError("episode checksum mismatch")
    rows = [json.loads(line) for line in raw.splitlines()]
    if len(rows) != meta["rows"] or not rows:
        raise ValueError("row count mismatch or empty episode")
    n = len(meta["config"]["home"])
    last = -float("inf")
    for i, row in enumerate(rows):
        if row["step"] != i or not row["t_robot_s"] > last:
            raise ValueError("invalid step order or non-monotonic time")
        last = row["t_robot_s"]
        for key in ("observation.q", "observation.dq", "action.q", "target.q"):
            a = np.asarray(row[key], float)
            if a.shape != (n,) or not np.isfinite(a).all():
                raise ValueError("invalid recorded vector")
    return meta, rows


def export_npz(path, output):
    meta, rows = read_episode(path)
    # Keep all rows and validity mask: dropping HOLD rows silently breaks temporal adjacency.
    with open(output, "xb") as f:
        np.savez_compressed(f, observation=np.array([r["observation.q"] for r in rows]),
            action=np.array([r["action.q"] for r in rows]),
            target=np.array([r["target.q"] for r in rows]),
            gripper_observation=np.array([r["observation.gripper"] for r in rows]),
            gripper_action=np.array([r["action.gripper"] for r in rows]),
            timestamp=np.array([r["t_robot_s"] for r in rows]),
            valid=np.array([r["sample_weight"] for r in rows], dtype=bool),
            metadata_json=np.array(json.dumps(meta)))
