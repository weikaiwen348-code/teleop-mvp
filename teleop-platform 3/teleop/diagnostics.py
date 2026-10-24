"""Source-project diagnostics and serial self-check, never physical commissioning."""
from datetime import datetime, timezone
from pathlib import Path
import html
import importlib.metadata
import json
import platform
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]


def unique_output(prefix):
    return ROOT / 'runs' / (prefix + '-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:6])


def doctor():
    checks = []
    checks.append({'name':'Python 3.10+', 'ok':sys.version_info >= (3,10), 'detail':sys.version.split()[0]})
    for name in ('numpy','mujoco'):
        try:
            version = importlib.metadata.version(name)
            __import__(name)
            checks.append({'name':name, 'ok':name!='mujoco' or version=='3.3.7', 'detail':version})
        except Exception as exc:
            checks.append({'name':name,'ok':False,'detail':str(exc)})
    required = ['teleop/assets/franka_emika_panda/scene.xml','teleop/assets/franka_emika_panda/LICENSE',
        'teleop/web/index.html','teleop/web/app.js','teleop/web/control-worker.js','teleop/web/three.module.js']
    missing = [name for name in required if not (ROOT/name).is_file()]
    checks.append({'name':'模型与网页资源','ok':not missing,'detail':missing or 'present'})
    if all(c['ok'] for c in checks):
        try:
            from .panda import PandaRobot, panda_config
            robot = PandaRobot(panda_config())
            try:
                checks.append({'name':'Panda 模型加载','ok':robot.model.nu==8 and robot.model.nv==9,
                    'detail':{'actuators':robot.model.nu,'velocity_dofs':robot.model.nv}})
            finally:
                robot.close()
        except Exception as exc:
            checks.append({'name':'Panda 模型加载','ok':False,'detail':str(exc)})
    return {'passed':all(c['ok'] for c in checks),'platform':platform.platform(),
        'python_executable':sys.executable,'checks':checks,
        'scope':'local dependencies/model only; browser and physical hardware not certified'}


def quickcheck(output=None):
    out = Path(output) if output else unique_output('checks')
    out.mkdir(parents=True, exist_ok=False)
    result = {'scope':'local simulation and software checks; no real robot or WAN','passed':False,
        'created_utc':datetime.now(timezone.utc).isoformat(),'checks':[]}
    try:
        environment = doctor()
        (out/'environment.json').write_text(json.dumps(environment,ensure_ascii=False,indent=2),encoding='utf-8')
        result['checks'].append({'name':'环境与模型','passed':environment['passed']})
        if not environment['passed']:
            raise RuntimeError('环境检查失败，见 environment.json；先安装演示依赖。')
        tests = subprocess.run([sys.executable,str(ROOT/'tools/run_tests.py'),'--output',str(out/'tests')],
            cwd=ROOT,capture_output=True,text=True,timeout=180)
        (out/'test-runner.log').write_text(tests.stdout+tests.stderr,encoding='utf-8')
        result['checks'].append({'name':'全部测试且无跳过','passed':tests.returncode==0})
        if tests.returncode:
            raise RuntimeError('测试失败或存在跳过，见 tests/tests.log；不把跳过当作通过。')
        from .panda import panda_config
        from .simulation import run_sim
        from .recording import export_npz
        from .quality import write_quality_report
        episode = out/'panda-episode'
        sim = run_sim(panda_config(),episode,duration=2,backend='panda',delay_ms=0,jitter_ms=0)
        export_npz(episode,episode/'episode.npz')
        quality,_ = write_quality_report(episode)
        good = quality['integrity_passed'] and sim['active_steps']>100
        result['checks'].append({'name':'Panda 运动、采集与 NPZ 一致性','passed':good})
        if not good:
            raise RuntimeError('Panda 仿真或数据检查未通过。')
        udp = subprocess.run([sys.executable,'-m','examples.loopback_validation','--backend','panda',
            '--output',str(out/'udp')],cwd=ROOT,capture_output=True,text=True,timeout=30)
        (out/'udp.log').write_text(udp.stdout+udp.stderr,encoding='utf-8')
        result['checks'].append({'name':'本机 UDP 跟随与断流保持','passed':udp.returncode==0})
        if udp.returncode:
            raise RuntimeError('UDP 检查失败，见 udp.log；关闭其他重负载程序后排查。')
        result['passed'] = True
    except Exception as exc:
        result['error'] = str(exc)
    (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    items=''.join('<li>'+html.escape(c['name'])+'：'+('通过' if c['passed'] else '未通过')+'</li>' for c in result['checks'])
    page='<!doctype html><meta charset="utf-8"><title>软件自检报告</title><style>body{max-width:850px;margin:40px auto;padding:20px;font:18px/1.9 sans-serif;color:#203543}</style>'
    page+='<h1>'+('本机软件自检通过' if result['passed'] else '自检未全部通过')+'</h1><ul>'+items+'</ul>'
    page+='<p>'+html.escape(result.get('error','可以继续手动演示，并在实际答辩电脑上彩排。'))+'</p>'
    page+='<p>本报告没有验收实体机器人、跨地域网络、力反馈或任务成功率。网页的实际显示仍需在你的电脑上打开确认。</p>'
    (out/'report.html').write_text(page,encoding='utf-8')
    return result,out
