import tempfile
import unittest
from pathlib import Path
import numpy as np
try:
    import mujoco
except ImportError:
    mujoco = None
from teleop.panda import PandaRobot, panda_config
from teleop.manual import ManualEngine
from teleop.recording import read_episode


@unittest.skipIf(mujoco is None, "optional Panda dependencies not installed")
class PandaTests(unittest.TestCase):
    def test_public_model_and_native_gripper_tracking(self):
        robot = PandaRobot(panda_config())
        try:
            self.assertEqual(robot.model.nu, 8)
            self.assertEqual(robot.model.nv, 9)
            self.assertAlmostEqual(robot.model.opt.gravity[2], -9.81)
            target = np.array(robot.c.home); target[0] = .2
            for _ in range(200):
                robot.command(target, 1.0, .01)
            self.assertLess(abs(robot.read()['q'][0] - .2), .01)
            self.assertGreater(robot.read()['gripper'], .9)
            for _ in range(150):
                robot.command(target, 0.0, .01)
            self.assertLess(robot.read()['gripper'], .1)
        finally:
            robot.close()

    def test_model_ranges_reject_incompatible_configuration(self):
        config = panda_config(); config.upper[3] = 0.5
        with self.assertRaisesRegex(ValueError, 'model ranges'):
            PandaRobot(config)

    def test_local_control_rearm_and_complete_export(self):
        with tempfile.TemporaryDirectory() as directory:
            engine = ManualEngine(Path(directory) / 'episode')
            engine.begin()
            try:
                state = engine.snapshot(False)
                self.assertNotIn('poses', state)
                payload = dict(session=state['session'], lease=state['lease'],
                    epoch=state['epoch'], q=state['q'], gripper=0, deadman=True, client_id='test', input_seq=0)
                self.assertTrue(engine.command(payload)['accepted'])
                engine.local_action('estop')
                state = engine.snapshot(False)
                payload.update(session=state['session'], lease=state['lease'], epoch=state['epoch'], input_seq=1)
                self.assertFalse(engine.command(payload)['accepted'])
                engine.local_action('reset')
                self.assertEqual(engine.control.mode, 'DISARMED')
                state = engine.snapshot(False)
                payload.update(lease=state['lease'], epoch=state['epoch'], q=state['q'], input_seq=2)
                self.assertTrue(engine.command(payload)['accepted'])
            finally:
                engine.local_action('finish')
                engine.close()
            meta, rows = read_episode(Path(directory) / 'episode')
            self.assertTrue(meta['complete'])
            self.assertGreater(len(rows), 0)
            self.assertIsNone(meta['success'])
            with np.load(Path(directory) / 'episode' / 'episode.npz') as data:
                self.assertEqual(data['observation'].shape[1], 7)

    def test_local_input_rejects_coerced_angles_and_wrong_session(self):
        with tempfile.TemporaryDirectory() as directory:
            engine = ManualEngine(Path(directory) / 'episode')
            engine.begin()
            try:
                state = engine.snapshot(False)
                payload = dict(session=state['session'], lease=state['lease'],
                    epoch=state['epoch'], q=['0'] * 7, gripper=0, deadman=True)
                with self.assertRaisesRegex(ValueError, 'numeric'):
                    engine.command(payload)
                payload.update(q=state['q'], session='previous_session')
                with self.assertRaisesRegex(ValueError, 'session'):
                    engine.command(payload)
            finally:
                engine.close()
