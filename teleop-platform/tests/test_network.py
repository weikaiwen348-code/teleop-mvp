import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest


class NetworkTests(unittest.TestCase):
    def test_virtual_source_starts_at_home_after_slow_backend_start(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d); key=path/'test.key'; key.write_bytes(os.urandom(32))
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
                sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
            client=subprocess.Popen([sys.executable,'-m','teleop','client','--keyfile',str(key),
                '--port',str(port),'--duration','3.8','--virtual'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            server=None
            try:
                time.sleep(1.6)
                server=subprocess.Popen([sys.executable,'-m','teleop','server','--output',str(path/'episode'),
                    '--keyfile',str(key),'--port',str(port),'--duration','3'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                _,err=client.communicate(timeout=5)
                self.assertEqual(client.returncode,0,err)
                out,err=server.communicate(timeout=5)
                self.assertEqual(server.returncode,0,err)
                result=json.loads(out)
                self.assertGreater(result['accepted'],130)
                self.assertEqual(result['rejected'],0)
                self.assertEqual(result['final_mode'],'HOLD')
            finally:
                for process in (client,server):
                    if process is not None and process.poll() is None:
                        process.kill(); process.communicate()

    def test_two_process_udp_and_sender_exit(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)
            key=path/'test.key'; key.write_bytes(os.urandom(32))
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
                s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
            server=subprocess.Popen([sys.executable,'-m','teleop','server','--output',str(path/'episode'),
                '--keyfile',str(key),'--port',str(port),'--duration','3'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            try:
                time.sleep(.25)
                c=subprocess.run([sys.executable,'-m','teleop','client','--keyfile',str(key),'--port',str(port),
                    '--duration','1.5','--virtual'],capture_output=True,text=True,timeout=5)
                self.assertEqual(c.returncode,0,c.stderr)
                out,err=server.communicate(timeout=5)
                self.assertEqual(server.returncode,0,err)
                result=json.loads(out)
                self.assertGreater(result['accepted'],50)
                self.assertEqual(result['final_mode'],'HOLD')
                self.assertEqual(result['final_reason'],'input_timeout')
                self.assertIsNotNone(json.loads(c.stdout)['ack_p95_ms'])
            finally:
                if server.poll() is None:
                    server.kill(); server.communicate()


if __name__=='__main__': unittest.main()
