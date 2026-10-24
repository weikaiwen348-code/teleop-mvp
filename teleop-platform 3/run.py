#!/usr/bin/env python3
"""Beginner launcher. Creates only this project's .venv, never a system env."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import venv
import webbrowser

ROOT = Path(__file__).resolve().parent


def environment():
    if sys.version_info < (3,10):
        raise RuntimeError('需要 Python 3.10+。已有 Conda 的同学可执行：conda create -n teleop python=3.11 -y，然后 conda activate teleop。')
    folder = ROOT / '.venv'
    python = folder / ('Scripts/python.exe' if os.name=='nt' else 'bin/python')
    if not python.exists():
        print('首次准备：正在创建本项目独立的 .venv 环境……',flush=True)
        venv.EnvBuilder(with_pip=True).create(folder)
    probe = subprocess.run([str(python),'-c',
        "import sys,numpy,mujoco; assert sys.version_info >= (3,10); assert mujoco.__version__=='3.3.7'"],
        cwd=ROOT,capture_output=True,text=True)
    stamp = folder/'teleop-install.json'
    digest = hashlib.sha256((ROOT/'pyproject.toml').read_bytes()).hexdigest()
    try:
        installed = json.loads(stamp.read_text(encoding='utf-8')).get('pyproject_sha256') == digest
    except (OSError,ValueError):
        installed = False
    if probe.returncode or not installed:
        print('正在安装/更新演示依赖（首次需要联网）。安装失败时保留下面的完整错误。',flush=True)
        install = subprocess.run([str(python),'-m','pip','install','--disable-pip-version-check',
                                  '-e',str(ROOT)+'[demo]'],cwd=ROOT)
        if install.returncode:
            raise RuntimeError('依赖安装失败。检查网络和 Python 版本后重新运行；不用删除工程和 runs 数据。')
        stamp.write_text(json.dumps({'pyproject_sha256':digest}),encoding='utf-8')
    return python


def execute(action, no_browser=False):
    from teleop.diagnostics import doctor, quickcheck, unique_output
    if action=='demo':
        from teleop.manual import serve_manual
        from teleop.quality import write_quality_report
        output = unique_output('manual')
        print('网页打开后依次：开启跟随 → 小幅拖关节/夹爪 → 暂停/恢复 → 结束并保存。',flush=True)
        summary = serve_manual(output,port=0,open_browser=not no_browser,auto_exit=True)
        result,report = write_quality_report(output,output/'quality-report')
        print('数据检查报告：'+str(report/'report.html'),flush=True)
        if not no_browser:
            webbrowser.open((report/'report.html').as_uri())
        return 0 if summary.get('complete') and result['integrity_passed'] else 1
    if action=='check':
        print('开始逐项自检；请先关闭正在运行的演示和高负载程序。',flush=True)
        result,out = quickcheck()
        print(('自检通过。' if result['passed'] else '自检未全部通过。')+'报告：'+str(out/'report.html'),flush=True)
        if not no_browser:
            webbrowser.open((out/'report.html').as_uri())
        return 0 if result['passed'] else 1
    if action=='report':
        from teleop.quality import write_quality_report
        episodes = sorted((ROOT/'runs').glob('*/metadata.json'),key=lambda p:p.stat().st_mtime,reverse=True)
        if not episodes:
            raise RuntimeError('还没有自己的采集记录。先选择 1 演示并保存一次。')
        result,out = write_quality_report(episodes[0].parent,unique_output('quality'))
        print('检查的采集目录：'+str(episodes[0].parent))
        print('报告：'+str(out/'report.html'))
        if not no_browser:
            webbrowser.open((out/'report.html').as_uri())
        return 0 if result['integrity_passed'] else 1
    result = doctor()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['passed'] else 1


def main():
    p=argparse.ArgumentParser(description='机器人仿真新手入口：环境安装、演示、自检、数据报告')
    p.add_argument('action',nargs='?',choices=['menu','demo','check','report','doctor'],default='menu')
    p.add_argument('--no-browser',action='store_true',help='不自动打开浏览器')
    p.add_argument('--current-python',action='store_true',help=argparse.SUPPRESS)
    a=p.parse_args()
    os.chdir(ROOT)
    action=a.action
    if action=='menu':
        print('\n机器人遥操作仿真 v0.3\n1 开始演示并采集\n2 自动检查软件与数据链路\n3 检查最近一次采集\n4 打开零基础指南\n0 退出\n')
        choice=input('输入数字后回车（直接回车选 1）：').strip() or '1'
        if choice=='0':return 0
        if choice=='4':
            webbrowser.open((ROOT/'START_HERE.html').as_uri());return 0
        if choice not in ('1','2','3'):
            print('请选择 0～4。');return 1
        action={'1':'demo','2':'check','3':'report'}[choice]
    if not a.current_python:
        python=environment()
        command=[str(python),str(Path(__file__).resolve()),action,'--current-python']
        if a.no_browser:command.append('--no-browser')
        return subprocess.run(command,cwd=ROOT).returncode
    return execute(action,a.no_browser)


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print('\n操作已中断。原始记录保留在 runs 文件夹。')
        raise SystemExit(130)
    except Exception as exc:
        print('\n未完成：'+str(exc),file=sys.stderr)
        print('请把完整错误文字交给环境负责人；不要修改数据来绕过检查。',file=sys.stderr)
        raise SystemExit(1)
