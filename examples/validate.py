"""Reproduce software evidence. Synthetic duration is not wall-clock endurance."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys
from teleop.config import load_config
from teleop.simulation import run_sim


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',required=True)
    a=p.parse_args()
    out=Path(a.output); out.mkdir(parents=True,exist_ok=False)
    tests=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],capture_output=True,text=True)
    (out/'tests.txt').write_text(tests.stdout+tests.stderr)
    if tests.returncode: raise SystemExit(tests.returncode)
    config=load_config()
    cases=[('baseline',dict(duration=6,delay_ms=0,jitter_ms=0)),
           ('delay_loss',dict(duration=6,delay_ms=20,jitter_ms=5,loss=.05)),
           ('blackout',dict(duration=6,delay_ms=5,jitter_ms=1,blackout_at=3)),
           ('expired',dict(duration=3,delay_ms=100,jitter_ms=0)),
           ('mujoco',dict(duration=6,delay_ms=5,backend='mujoco')),
           ('paced_mujoco',dict(duration=6,backend='mujoco',realtime=True)),
           ('long_sim',dict(duration=600,delay_ms=5,jitter_ms=1))]
    results={name:run_sim(config,out/name,**kwargs) for name,kwargs in cases}
    # Keep pass criteria about implemented behavior, not artificial plant accuracy.
    checks={
      'baseline_active':results['baseline']['active_steps']>500,
      'delay_loss_active':results['delay_loss']['active_steps']>500,
      'blackout_hold':results['blackout']['final_reason']=='input_timeout',
      'blackout_under_200ms':results['blackout']['blackout_to_hold_ms']<=200,
      'expired_never_arms':results['expired']['commands_accepted']==0,
      'mujoco_active':results['mujoco']['active_steps']>500,
      'long_sim_active':results['long_sim']['active_steps']>59000,
    }
    report={'environment':{'python':sys.version,'platform':platform.platform(),
         'numpy':importlib.metadata.version('numpy'),'mujoco':importlib.metadata.version('mujoco')},
         'results':results,'checks':checks,'all_passed':all(checks.values())}
    (out/'validation.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    if not report['all_passed']: raise SystemExit(1)


if __name__=='__main__': main()
