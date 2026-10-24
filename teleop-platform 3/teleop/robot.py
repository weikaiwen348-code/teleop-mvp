from typing import Protocol
from contextlib import nullcontext
import numpy as np
from .config import vector


class Robot(Protocol):
    def read(self): ...
    def command(self, q, gripper, dt): ...
    def stop(self): ...
    def close(self): ...


class SimRobot:
    """First-order joint plant. No inertia, contacts, FK or real-robot accuracy claim."""
    def __init__(self, config):
        self.c = config
        self.q = np.array(config.home, float)
        self.dq = np.zeros(config.n)
        self.gripper = 0.0

    def read(self):
        return {"q": self.q.copy(), "dq": self.dq.copy(), "gripper": self.gripper}

    def command(self, q, gripper, dt):
        target = vector(q, self.c.n, "target")
        old = self.q.copy()
        self.q += (target-self.q)*(1-np.exp(-dt/0.025))
        self.dq = (self.q-old)/dt
        self.gripper += float(np.clip(gripper-self.gripper, -dt, dt))

    def stop(self):
        self.dq[:] = 0

    def close(self):
        self.stop()


class RealRobotUnavailable:
    def __init__(self, *args, **kwargs):
        raise RuntimeError("Real motion disabled: hardware model, local servo, limits, stop path and commissioning are unverified. See docs/HARDWARE.md")


class MujocoRobot:
    """Self-contained generic chain for integration tests, NOT a Panda/UR digital twin.

    Collision-free independent hinge dynamics use inertia and damping. Gripper is
    a software scalar only. Replace model and actuator mapping before real validation.
    """
    def __init__(self, config, viewer=False):
        import mujoco
        self.mj = mujoco
        self.c = config
        bodies = []
        for i in range(config.n):
            axis = "0 0 1" if i % 2 == 0 else "0 1 0"
            bodies.append(f'<body pos="0 0 0.16"><joint name="j{i}" axis="{axis}" range="{config.lower[i]} {config.upper[i]}" damping="3" armature="0.5"/><geom type="capsule" fromto="0 0 0 0 0 0.16" size="0.025" mass="0.3" contype="0" conaffinity="0" rgba="0.2 0.5 0.8 1"/>')
        acts = ''.join(f'<position joint="j{i}" kp="80" kv="15"/>' for i in range(config.n))
        xml = '<mujoco model="generic_chain_not_hardware"><compiler angle="radian"/><option timestep="0.002" gravity="0 0 0"/><worldbody><light pos="1 1 3"/>' + ''.join(bodies) + '</body>'*config.n + '</worldbody><actuator>' + acts + '</actuator></mujoco>'
        self.model = mujoco.MjModel.from_xml_string(xml)
        self.data = mujoco.MjData(self.model)
        self.data.qpos[:] = config.home
        self.data.ctrl[:] = config.home
        self.gripper = 0.0
        mujoco.mj_forward(self.model, self.data)
        self.viewer = None
        if viewer:
            import mujoco.viewer
            self.viewer = mujoco.viewer.launch_passive(self.model, self.data)

    def read(self):
        return {"q": self.data.qpos.copy(), "dq": self.data.qvel.copy(), "gripper": self.gripper}

    def command(self, q, gripper, dt):
        with self.viewer.lock() if self.viewer else nullcontext():
            self.data.ctrl[:] = vector(q, self.c.n, "q")
            steps = max(1, int(np.ceil(dt/0.002)))
            self.model.opt.timestep = dt/steps
            self.mj.mj_step(self.model, self.data, nstep=steps)
        self.gripper += float(np.clip(gripper-self.gripper, -dt, dt))
        if self.viewer:
            self.viewer.sync()

    def stop(self):
        # A numerical freeze; NOT a physically realizable certified stop.
        self.data.ctrl[:] = self.data.qpos
        self.data.qvel[:] = 0
        self.mj.mj_forward(self.model, self.data)

    def close(self):
        self.stop()
        if self.viewer:
            self.viewer.close()


def make_robot(config, backend="toy", viewer=False):
    if backend == "toy":
        return SimRobot(config)
    if backend == "mujoco":
        return MujocoRobot(config, viewer)
    if backend == "panda":
        from .panda import PandaRobot
        return PandaRobot(config, viewer)
    return RealRobotUnavailable()
