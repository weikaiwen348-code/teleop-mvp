# 机器人遥操作软件原型 · v0.3.0

**全组先打开根目录的 `START_HERE.html`。不需要先学代码。** Markdown 版：[零基础操作指南](docs/TEAM_GUIDE.md)。

已经完成：Panda 三维仿真、浏览器关节与夹爪输入、关节映射、运动约束、断流保持、轨迹记录、NPZ 导出、自动自检与数据报告。**尚未接通真实 Franka/UR；没有完成实体 GELLO 标定、力反馈、相机同步或跨地域实测。**

## 第一次使用

1. 完整解压本工程，找到 `START_HERE.html` 和 `run.py` 所在文件夹。
2. 准备 Python 3.10+（建议使用已有的 3.11/3.12 环境）。macOS 双击 `START.command`，Windows 双击 `START.bat`，Linux 在工程目录执行 `bash START.sh`。
3. 输入 `2` 回车做自动自检；通过后再次启动，输入 `1` 回车开始演示。
4. 点击网页的“结束并保存”；等待结果，启动器会自动退出服务并生成数据报告。

首次自动创建本工程的 `.venv` 并联网安装依赖。不会要求你手动选端口、起采集文件夹名或编写导出命令。每次数据保存在新的 `runs/` 子目录。只读取说明、PPT 和视频无需安装 Python。

命令行等价入口：

```bash
python run.py check
python run.py demo
python run.py report
```

在 macOS/Linux 若 `python` 不存在，用 `python3`。macOS/Windows 启动入口已提供，但本次实际自动验证环境为 Linux + Python 3.12；仍需在答辩电脑彩排。

## 这次审查交付

- [审查与修复报告](reports/AUDIT_V03.md)：依据、缺陷、已完成修复、测试证据、未完成事项。
- [零基础指南](docs/TEAM_GUIDE.md)：每一步点什么、成功画面、出错处理、数据和术语。
- [现场必须做的事](docs/ON_SITE_ONLY.md)：可填写的设备信息与现场责任边界。
- [团队任务表](docs/TEAM_TASKS.md)：现在只需做的少量任务。
- [全部材料索引](docs/MATERIAL_INDEX.md)；[逐文件清单](reports/FILE_AUDIT.md)；[版本区别](docs/VERSION_COMPARISON.md)。
- [答辩 PPT](defense/robot-teleop-defense.pptx)、[约 40 秒视频](defense/panda-teleop-demo.mp4)、[讲稿与问答](defense/defense-script-and-qa.md)、[当天操作卡](defense/defense-operation-card.md)。

v0.3 修复旧使能标记检查、网页重复/跨页面指令、保存失败提示、配置与 NPZ 一致性检查等问题。严格测试 41 项通过、0 跳过，另有真实浏览器正常/失败流程、独立安装包与启动器集成检查。证据见报告；这些是本机软件检查。

## GitHub 状态

2026-10-04，目标 `weikaiwen348-code/teleop-mvp` 仍返回 404，可访问仓库列表为空。**本次审查基于上一版已交付的 172 文件工程，未读取 GitHub 最新提交，未上传本次更新。** 不能把本地交付称为远端审查完成。仓库负责人只需确认正确地址和连接访问权，之后可继续比对、合并和提交。详见 [GitHub 说明](docs/GITHUB_UPDATE.md)。

## 开发者入口（普通组员可跳过）

```bash
python -m pip install -e '.[demo]'
python -m teleop doctor
python -m teleop quickcheck
python -m teleop --help
```

自检需要完整源码目录中的 `tools/`、`tests/`、`examples/`；wheel 是运行包，不含答辩材料或完整自检脚本。可选自动浏览器验证另见 [说明](examples/README_UI_CHECK.md)。

技术资料：[架构](docs/ARCHITECTURE.md)、[数据协议](docs/DATA_SCHEMA.md)、[界面](docs/MANUAL_UI.md)、[硬件接入](docs/HARDWARE.md)、[来源和许可](docs/SOURCES.md)。旧版入口留在 `docs/history/` 仅供追溯，以本页和当前新手指南为准。
