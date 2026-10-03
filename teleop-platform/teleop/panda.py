"""Franka Panda simulation using the unchanged MuJoCo Menagerie model."""
from pathlib import Path
import json
import numpy as np
from .config import Config, vector

MODEL_DIR = Path(__file__).parent / "assets" / "franka_emika_panda"


def panda_config():
    # Conservative demonstration workspace inside the model's joint ranges.
    return Config("franka_panda_menagerie_sim", [0,0,0,-1.57079,0,1.57079,-.7853],
        [-2.5,-1.5,-2.5,-2.8,-2.5,.1,-2.5], [2.5,1.5,2.5,-.2,2.5,3.4,2.5],
        [.4]*7, [1.0]*7).validate()


class PandaRobot:
    def __init__(self, config, viewer=False):
        import mujoco
        if config.n != 7:
            raise ValueError("Panda requires 7 arm joints")
        self.mj = mujoco
        self.c = config
        self.model = mujoco.MjModel.from_xml_path(str(MODEL_DIR / "scene.xml"))
        self.data = mujoco.MjData(self.model)
        self.joint_ids = [mujoco.mj_name2id(self.model,mujoco.mjtObj.mjOBJ_JOINT,f"joint{i}") for i in range(1,8)]
        self.qadr = self.model.jnt_qposadr[self.joint_ids]
        self.vadr = self.model.jnt_dofadr[self.joint_ids]
        self.act_ids = [mujoco.mj_name2id(self.model,mujoco.mjtObj.mjOBJ_ACTUATOR,f"actuator{i}") for i in range(1,8)]
        self.grip_act = mujoco.mj_name2id(self.model,mujoco.mjtObj.mjOBJ_ACTUATOR,"actuator8")
        self.finger_adr = [self.model.jnt_qposadr[mujoco.mj_name2id(self.model,mujoco.mjtObj.mjOBJ_JOINT,f"finger_joint{i}")] for i in (1,2)]
        actual_ranges = self.model.jnt_range[self.joint_ids]
        if np.any(np.array(config.lower)<actual_ranges[:,0]) or np.any(np.array(config.upper)>actual_ranges[:,1]):
            raise ValueError("configuration exceeds Panda model ranges")
        mujoco.mj_resetDataKeyframe(self.model,self.data,0)
        self.data.qpos[self.qadr] = config.home
        self.data.ctrl[self.act_ids] = config.home
        mujoco.mj_forward(self.model,self.data)
        self.viewer = None
        if viewer:
            import mujoco.viewer
            self.viewer = mujoco.viewer.launch_passive(self.model,self.data)

    def read(self):
        opening = float(np.sum(self.data.qpos[self.finger_adr]))
        return {"q":self.data.qpos[self.qadr].copy(), "dq":self.data.qvel[self.vadr].copy(),
                "gripper":float(np.clip(1-opening/.08,0,1))}

    def command(self, q, gripper, dt):
        self.data.ctrl[self.act_ids] = vector(q,7,"Panda target")
        self.data.ctrl[self.grip_act] = 255*(1-float(gripper))
        count=max(1,int(np.ceil(dt/.002)))
        self.model.opt.timestep=dt/count
        self.mj.mj_step(self.model,self.data,nstep=count)
        if self.viewer:
            self.viewer.sync()

    def stop(self):
        # Simulation-only numerical freeze. Real commissioning needs a physical stop path.
        self.data.ctrl[self.act_ids]=self.data.qpos[self.qadr]
        self.data.qvel[:]=0
        self.mj.mj_forward(self.model,self.data)

    def close(self):
        self.stop()
        if self.viewer:
            self.viewer.close()

    def visual_model(self):
        """Compiled meshes plus geom indices, preserving MuJoCo mesh transforms."""
        geoms=[]; meshes={}
        for i in range(self.model.ngeom):
            if self.model.geom_group[i]!=2 or self.model.geom_dataid[i]<0:
                continue
            mesh=int(self.model.geom_dataid[i])
            if mesh not in meshes:
                va,nv=int(self.model.mesh_vertadr[mesh]),int(self.model.mesh_vertnum[mesh])
                fa,nf=int(self.model.mesh_faceadr[mesh]),int(self.model.mesh_facenum[mesh])
                meshes[mesh]={"vertices":self.model.mesh_vert[va:va+nv].ravel().tolist(),
                              "faces":self.model.mesh_face[fa:fa+nf].ravel().tolist()}
            mat=int(self.model.geom_matid[i])
            color=self.model.mat_rgba[mat] if mat>=0 else self.model.geom_rgba[i]
            geoms.append({"id":i,"mesh":mesh,"color":color.tolist()})
        return {"meshes":meshes,"geoms":geoms,"source":json.loads((MODEL_DIR/"SOURCE.json").read_text())}

    def visual_poses(self):
        return [{"id":i,"pos":self.data.geom_xpos[i].tolist(),"mat":self.data.geom_xmat[i].tolist()}
                for i in range(self.model.ngeom) if self.model.geom_group[i]==2]
