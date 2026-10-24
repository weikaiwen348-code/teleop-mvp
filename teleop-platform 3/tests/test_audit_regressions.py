import hashlib
import json
from pathlib import Path
import re
import socket
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import numpy as np
from teleop.config import load_config
from teleop.control import Controller
from teleop.protocol import Command
from teleop.recording import Recorder, export_npz, read_episode
from teleop.simulation import run_sim
from teleop.quality import inspect_quality
from teleop.manual import ManualEngine, create_manual_server
try:
    import mujoco
except ImportError:
    mujoco = None


class ControlRegressionTests(unittest.TestCase):
    def test_old_enable_generation_rejected_even_when_active(self):
        c=load_config(); ctrl=Controller(c)
        self.assertTrue(ctrl.receive(Command(0,c.home,0,True,ctrl.epoch),0,.12,c.home))
        self.assertFalse(ctrl.receive(Command(1,c.home,0,True,'old-epoch'),.01,.13,c.home))
        self.assertEqual(ctrl.last_rx,0)
        self.assertEqual(ctrl.last_seq,0)
        self.assertTrue(ctrl.receive(Command(2,c.home,0,True,ctrl.epoch),.02,.14,c.home))


class DataRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'ep'
        run_sim(load_config(),self.path,duration=.2,delay_ms=0,jitter_ms=0)

    def rewrite_rows(self, change):
        rows=[json.loads(x) for x in (self.path/'steps.jsonl').read_text().splitlines()]
        change(rows)
        raw=('\n'.join(json.dumps(x) for x in rows)+'\n').encode()
        (self.path/'steps.jsonl').write_bytes(raw)
        meta=json.loads((self.path/'metadata.json').read_text())
        meta['steps_sha256']=hashlib.sha256(raw).hexdigest()
        (self.path/'metadata.json').write_text(json.dumps(meta))

    def test_changed_config_rejected(self):
        meta=json.loads((self.path/'metadata.json').read_text())
        meta['config']['velocity']=[999]*7
        (self.path/'metadata.json').write_text(json.dumps(meta))
        with self.assertRaisesRegex(ValueError,'configuration checksum'):
            read_episode(self.path)

    def test_infinite_timestamp_rejected_even_with_matching_hash(self):
        self.rewrite_rows(lambda rows: rows[-1].update(t_robot_s=float('inf')))
        with self.assertRaisesRegex(ValueError,'time'):
            read_episode(self.path)

    def test_validity_must_match_mode(self):
        self.rewrite_rows(lambda rows: rows[0].update(mode='HOLD',sample_weight=1))
        with self.assertRaisesRegex(ValueError,'validity'):
            read_episode(self.path)

    def test_invalid_gripper_rejected(self):
        self.rewrite_rows(lambda rows: rows[0].update({'action.gripper':True}))
        with self.assertRaisesRegex(ValueError,'gripper'):
            read_episode(self.path)

    def test_npz_content_mismatch_detected(self):
        npz=self.path/'episode.npz';export_npz(self.path,npz)
        self.assertTrue(inspect_quality(self.path)['integrity_passed'])
        with np.load(npz,allow_pickle=False) as data:
            values={k:data[k].copy() for k in data.files}
        values['action'][0,0]+=1
        np.savez_compressed(npz,**values)
        result=inspect_quality(self.path)
        self.assertFalse(result['integrity_passed'])
        self.assertIn('NPZ',result['errors'][0])

    def test_failed_export_removes_partial_file_and_preserves_existing(self):
        dest=self.path/'episode.npz'
        def fail(stream,**kwargs):
            stream.write(b'partial');raise OSError('disk-full-test')
        with patch('teleop.recording.np.savez_compressed',side_effect=fail):
            with self.assertRaises(OSError):export_npz(self.path,dest)
        self.assertFalse(dest.exists())
        dest.write_bytes(b'existing')
        with self.assertRaises(FileExistsError):export_npz(self.path,dest)
        self.assertEqual(dest.read_bytes(),b'existing')

    def test_writer_rejects_append_after_close(self):
        writer=Recorder(Path(self.temp.name)/'other',load_config())
        writer.close(complete=False)
        with self.assertRaisesRegex(RuntimeError,'closed'):writer.append({})


@unittest.skipIf(mujoco is None,'Panda dependency not installed')
class LocalUIRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'ep'

    def engine(self):
        engine=ManualEngine(self.path);engine.begin();self.addCleanup(engine.close)
        return engine

    def payload(self,engine,seq,client='browser-1'):
        s=engine.snapshot(False)
        return dict(session=s['session'],lease=s['lease'],epoch=s['epoch'],q=s['q'],
            gripper=s['gripper'],deadman=True,client_id=client,input_seq=seq)

    def test_replay_and_second_browser_rejected(self):
        engine=self.engine()
        self.assertTrue(engine.command(self.payload(engine,0))['accepted'])
        with self.assertRaisesRegex(ValueError,'replayed'):
            engine.command(self.payload(engine,0))
        with self.assertRaisesRegex(ValueError,'另一页面'):
            engine.command(self.payload(engine,1,'browser-2'))
        engine.local_action('reset')
        self.assertTrue(engine.command(self.payload(engine,0,'browser-2'))['accepted'])

    def test_export_failure_is_not_success(self):
        engine=self.engine()
        with patch('teleop.manual.export_npz',side_effect=OSError('disk-full-test')):
            engine.local_action('finish');engine.close()
        self.assertTrue(engine.finalized.is_set())
        self.assertFalse(engine.summary['complete'])
        self.assertFalse(engine.summary['export_complete'])
        self.assertIn('disk-full-test',engine.snapshot()['error'])

    def test_busy_http_port_does_not_create_episode_or_engine(self):
        with socket.socket() as sock:
            sock.bind(('127.0.0.1',0));sock.listen();port=sock.getsockname()[1]
            with patch('teleop.manual.ManualEngine') as constructor:
                with self.assertRaises(OSError):create_manual_server(self.path,port)
                constructor.assert_not_called()
        self.assertFalse(self.path.exists())

    def test_non_object_http_body_returns_error_and_server_survives(self):
        server,engine=create_manual_server(self.path,0)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            url='http://127.0.0.1:'+str(server.server_port)
            with urlopen(url,timeout=3) as response:page=response.read().decode()
            token=re.search(r'window.CONTROL_TOKEN="([^"]+)"',page).group(1)
            request=Request(url+'/api/action',data=b'[]',headers={'X-Control-Token':token,'Content-Type':'application/json'})
            with self.assertRaises(HTTPError) as error:urlopen(request,timeout=3)
            self.assertEqual(error.exception.code,400)
            with urlopen(url+'/api/state',timeout=3) as response:
                self.assertIn('mode',json.load(response))
        finally:
            server.shutdown();server.server_close();engine.close();thread.join(timeout=3)


if __name__=='__main__':unittest.main()
