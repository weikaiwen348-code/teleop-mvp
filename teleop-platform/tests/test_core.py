import json
import tempfile
import unittest
from pathlib import Path
import numpy as np
from teleop.config import load_config, vector
from teleop.mapping import JointMap, fit_calibration
from teleop.protocol import Command, LeaseBook, encode, decode
from teleop.control import Controller
from teleop.recording import Recorder, read_episode, export_npz, make_row
from teleop.robot import SimRobot, RealRobotUnavailable
from teleop.simulation import run_sim


class MappingTests(unittest.TestCase):
    def test_sign_offset_gain(self):
        m = JointMap([-1,1],[.5,1],[2,.5],[0,.2])
        np.testing.assert_allclose(m.apply([.7,1.4]),[-.4,.4])

    def test_different_topology_rejected(self):
        with self.assertRaises(ValueError):
            JointMap.identity(7).apply([0]*6)

    def test_fit_independent_pose(self):
        rng=np.random.default_rng(2)
        x=rng.uniform(-1,1,(20,7)); a=np.array([1,-1,2,1,.5,-1,1]); b=np.arange(7)*.1
        mapping, residual=fit_calibration(x,x*a+b)
        z=rng.uniform(-1,1,(7,))
        np.testing.assert_allclose(JointMap(**mapping).apply(z),z*a+b,atol=1e-12)
        self.assertLess(max(residual),1e-12)

    def test_bad_excitation(self):
        with self.assertRaises(ValueError):
            fit_calibration(np.zeros((3,7)),np.zeros((3,7)))


class WireTests(unittest.TestCase):
    def test_roundtrip_and_tamper(self):
        key=b'x'*32
        packet=encode({'v':1,'kind':'hello'},key)
        self.assertEqual(decode(packet,key)['kind'],'hello')
        with self.assertRaises(ValueError): decode(packet[:-1]+b'x',key)
        with self.assertRaises(ValueError): decode(packet,b'y'*32)

    def test_size_and_nan(self):
        with self.assertRaises(ValueError): encode({'v':1,'x':float('nan')},b'x'*32)
        with self.assertRaises(ValueError): decode(b'x'*9000,b'x'*32)

    def test_malformed_command(self):
        for cmd in [Command(True,[0]*7,0,True),Command(1,[float('nan')]*7,0,True),
                    Command(1,[0]*6,0,True),Command(1,[0]*7,2,True),Command(1,[0]*7,0,'yes'),
                    Command(1,[10**400]*7,0,True),Command(1,['0']*7,0,True),Command(1,[False]*7,0,True)]:
            with self.assertRaises(ValueError): cmd.validate(7)

    def test_lease_without_clock_sync(self):
        book=LeaseBook(.12); token=book.issue(5000)
        self.assertAlmostEqual(book.check(book.session,token,5000.05),5000.12)
        with self.assertRaises(ValueError): book.check(book.session,token,5000.13)
        with self.assertRaises(ValueError): book.check('old_session',token,5000.05)


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.c=load_config(); self.ctrl=Controller(self.c); self.obs=np.array(self.c.home)

    def arm(self):
        cmd=Command(0,self.obs.tolist(),0,True,self.ctrl.epoch)
        self.assertTrue(self.ctrl.receive(cmd,0,.12,self.obs))

    def test_start_disarmed_and_alignment(self):
        bad=self.obs+.2
        self.assertFalse(self.ctrl.receive(Command(0,bad.tolist(),0,True,self.ctrl.epoch),0,.1,self.obs))
        self.assertEqual(self.ctrl.mode,'DISARMED')

    def test_replay_does_not_refresh_watchdog(self):
        self.arm()
        self.assertFalse(self.ctrl.receive(Command(0,self.obs.tolist(),0,True),.1,.22,self.obs))
        self.ctrl.step(.121,.01,self.obs)
        self.assertEqual(self.ctrl.reason,'input_timeout')

    def test_stale_packet_and_bad_data(self):
        self.arm()
        self.assertFalse(self.ctrl.receive(Command(1,self.obs.tolist(),0,True),.2,.19,self.obs))
        self.assertEqual(self.ctrl.last_seq,0)
        self.assertFalse(self.ctrl.receive(Command(2,[100]*7,0,True),.01,.13,self.obs))
        self.assertEqual(self.ctrl.last_seq,0)

    def test_timeout_latches_until_new_arm_epoch(self):
        self.arm(); old=self.ctrl.epoch
        self.ctrl.step(.13,.01,self.obs)
        self.assertEqual(self.ctrl.mode,'HOLD')
        self.assertFalse(self.ctrl.receive(Command(1,self.obs.tolist(),0,True,old),.14,.26,self.obs))
        self.assertTrue(self.ctrl.receive(Command(2,self.obs.tolist(),0,True,self.ctrl.epoch),.15,.27,self.obs))

    def test_deadman_and_estop(self):
        self.arm()
        self.ctrl.receive(Command(1,[100]*7,0,False),.01,.13,self.obs)
        self.assertEqual(self.ctrl.mode,'HOLD')
        self.ctrl.receive(Command(2,[100]*7,0,False,estop=True),.02,.14,self.obs)
        self.assertEqual(self.ctrl.mode,'ESTOP')
        self.assertFalse(self.ctrl.receive(Command(3,self.obs.tolist(),0,True,self.ctrl.epoch),.03,.15,self.obs))
        self.ctrl.reset_local(self.obs)
        self.assertEqual(self.ctrl.mode,'DISARMED')

    def test_control_deadline_fault(self):
        self.arm(); self.ctrl.step(.04,.04,self.obs)
        self.assertEqual(self.ctrl.reason,'control_deadline')

    def test_tracking_fault(self):
        self.arm(); self.ctrl.step(.01,.01,self.obs+.5)
        self.assertEqual(self.ctrl.reason,'tracking_error')

    def test_velocity_acceleration_and_joint_limits(self):
        self.arm(); previous_v=self.ctrl.v.copy()
        for i in range(1,3001):
            t=i*.01
            target=self.c.upper if (i//400)%2==0 else self.c.lower
            self.ctrl.receive(Command(i,target,0,True),t,t+.12,self.ctrl.q)
            q=self.ctrl.step(t,.01,self.ctrl.q)
            self.assertEqual(self.ctrl.mode,'ACTIVE')
            self.assertTrue(np.all(q>=np.array(self.c.lower)-1e-9))
            self.assertTrue(np.all(q<=np.array(self.c.upper)+1e-9))
            self.assertTrue(np.all(np.abs(self.ctrl.v)<=np.array(self.c.velocity)+1e-9))
            self.assertTrue(np.all(np.abs(self.ctrl.v-previous_v)<=np.array(self.c.acceleration)*.01+1e-9))
            previous_v=self.ctrl.v.copy()

    def test_real_motion_unavailable(self):
        with self.assertRaises(RuntimeError): RealRobotUnavailable()

    def test_constant_target_settles_without_limit_cycle(self):
        self.arm()
        target=self.obs.copy(); target[0]+=.3
        trace=[]
        for i in range(1,401):
            t=i*.01
            self.ctrl.receive(Command(i,target.tolist(),0,True),t,t+.12,self.ctrl.q)
            trace.append(self.ctrl.step(t,.01,self.ctrl.q)[0])
        self.assertLess(max(trace)-target[0],1e-8)
        self.assertLess(max(abs(x-target[0]) for x in trace[-100:]),1e-6)
        self.assertLess(abs(self.ctrl.v[0]),1e-6)


class EpisodeTests(unittest.TestCase):
    def test_complete_export_and_checksum(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'episode'
            summary=run_sim(load_config(),p,duration=.5,delay_ms=0,jitter_ms=0)
            self.assertGreater(summary['active_steps'],20)
            meta,rows=read_episode(p)
            self.assertEqual(len(rows),50)
            self.assertIsNone(meta['success'])
            export_npz(p,Path(d)/'data.npz')
            with np.load(Path(d)/'data.npz',allow_pickle=False) as a:
                self.assertEqual(a['action'].shape,(50,7))
            with (p/'steps.jsonl').open('a') as f: f.write('{}\n')
            with self.assertRaises(ValueError): read_episode(p)

    def test_incomplete_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'episode'; r=Recorder(p,load_config()); r.close(complete=False)
            with self.assertRaises(ValueError): read_episode(p)

    def test_blackout_stops_and_does_not_rearm(self):
        with tempfile.TemporaryDirectory() as d:
            s=run_sim(load_config(),Path(d)/'run',duration=2,blackout_at=1)
            self.assertGreater(s['active_steps'],50)
            self.assertEqual(s['final_reason'],'input_timeout')
            self.assertLessEqual(s['blackout_to_hold_ms'],200)

    def test_delay_exceeds_freshness_budget(self):
        with tempfile.TemporaryDirectory() as d:
            s=run_sim(load_config(),Path(d)/'run',duration=1,delay_ms=100,jitter_ms=0)
            self.assertEqual(s['commands_accepted'],0)

    def test_mujoco_integration(self):
        try: import mujoco
        except ImportError: self.skipTest('optional MuJoCo not installed')
        with tempfile.TemporaryDirectory() as d:
            s=run_sim(load_config(),Path(d)/'run',duration=.5,backend='mujoco',delay_ms=0,jitter_ms=0)
            self.assertGreater(s['active_steps'],20)
            self.assertEqual(s['final_mode'],'ACTIVE')


if __name__ == '__main__':
    unittest.main()
