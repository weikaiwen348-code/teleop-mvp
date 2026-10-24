#!/bin/bash
cd "$(dirname "$0")" || exit 1
teleop_python=""
for candidate in python3.11 python3.12 python3.13 python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' >/dev/null 2>&1; then
        teleop_python="$candidate"
        break
    fi
done
if [ -z "$teleop_python" ]; then
    echo "没有找到 Python 3.10+。请先阅读 START_HERE.html 的环境准备部分。"
    echo "已有 Conda：conda create -n teleop python=3.11 -y，然后 conda activate teleop"
    exit 1
fi
"$teleop_python" run.py "$@"
teleop_status=$?
if [ -t 0 ]; then
    read -r -p "流程结束。按回车关闭。" teleop_reply
fi
exit "$teleop_status"
