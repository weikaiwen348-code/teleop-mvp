"""Wall-clock localhost measurement. No claim about a LAN, WAN or physical robot."""
from pathlib import Path
import argparse
import json
import os
import socket
import subprocess
import sys
import tempfile
import time


def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',required=True)
    p.add_argument('--backend',choices=['toy','mujoco','panda'],default='toy')
    p.add_argument('--config')
    a=p.parse_args()
    out=Path(a.output); out.mkdir(parents=True,exist_ok=False)
    config_args=['--config',a.config] if a.config else []
    if a.backend=='panda' and not a.config:
        config_args=['--config',str(Path(__file__).parents[1]/'configs/panda_model.json')]
    with tempfile.TemporaryDirectory() as d:
        key=Path(d)/'session.key'; key.write_bytes(os.urandom(32))
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
            s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
        server=subprocess.Popen([sys.executable,'-m','teleop','server','--keyfile',str(key),
            '--port',str(port),'--output',str(out/'episode'),'--duration','5','--backend',a.backend,*config_args],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:
            time.sleep(.3)
            client=subprocess.run([sys.executable,'-m','teleop','client','--keyfile',str(key),
                '--port',str(port),'--virtual','--duration','3',*config_args],capture_output=True,text=True,timeout=6)
            stdout,stderr=server.communicate(timeout=7)
            if server.returncode or client.returncode:
                raise RuntimeError(stderr+client.stderr)
            result={'server':json.loads(stdout),'client':json.loads(client.stdout),'backend':a.backend,'scope':'localhost UDP; wall time; simulated plant'}
            rows=[json.loads(x) for x in (out/'episode'/'steps.jsonl').read_text().splitlines()]
            active=[r for r in rows if r['mode']=='ACTIVE']
            held=[r for r in rows if r['event']=='input_timeout']
            result['last_accepted_packet_to_hold_ms']=(held[0]['t_robot_s']-active[-1]['rx_robot_s'])*1000 if active and held else None
            result['checks']={
                'motion_commands_accepted':result['server']['accepted']>50,
                'sender_exit_hold':result['server']['final_mode']=='HOLD' and result['server']['final_reason']=='input_timeout',
                'hold_event_recorded':result['last_accepted_packet_to_hold_ms'] is not None,
            }
            result['passed']=all(result['checks'].values())
            (out/'loopback.json').write_text(json.dumps(result,indent=2))
            if not result['passed']:
                raise RuntimeError('loopback behavior failed; retained result: '+str(result['checks']))
            print(json.dumps(result,indent=2))
        finally:
            if server.poll() is None: server.kill(); server.communicate()


if __name__=='__main__': main()
