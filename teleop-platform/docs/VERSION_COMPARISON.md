# v0.1 → v0.2 版本对照

比较对象是原始两份交付压缩包，按文件字节核对。不是 GitHub 分支差异；当前无法读取旧仓库。新手解读见 [TEAM_GUIDE.md](TEAM_GUIDE.md)。

## 结论与统计

v0.1 建立输入、映射、通信、软件控制与数据保存闭环；v0.2 加入公开 Panda 模型、浏览器界面、答辩资料，并修正固定目标过冲和后端慢启动问题。软件版本从 0.1.0 变为 0.2.0。

| 原始包文件统计 | 数量 |
|---|---:|
| v0.1 | 39 |
| v0.2 | 168 |
| 新增 | 129 |
| 修改 | 12 |
| 原样保留 | 27 |
| 删除 | 0 |

模型网格、图片、字体也按文件计数，不能据此计算项目完成百分比。统计不含本次后加的团队说明。

## 12 个修改文件

| 文件 | 变化 |
|---|---|
| README.md | 新增 Panda、浏览器与答辩入口和范围说明 |
| pyproject.toml | 版本 0.2.0、demo 依赖、模型与网页资源打包 |
| teleop/__init__.py | 版本标识更新 |
| teleop/cli.py | ui 命令、panda 后端、默认 Panda 配置选择 |
| teleop/robot.py | Panda 后端加入统一入口 |
| teleop/control.py | 固定目标附近的制动约束 |
| teleop/network.py | 首次收到后端状态后才推进虚拟轨迹 |
| tests/test_core.py | 固定目标收敛回归测试 |
| tests/test_network.py | 慢启动回归测试 |
| examples/loopback_validation.py | 支持 Panda/配置选择，增加接受运动与退出后 HOLD 检查 |
| docs/ARCHITECTURE.md | 补充界面、绘图与心跳路径 |
| docs/SOURCES.md | 新资源来源与许可证说明 |

## 主要新增内容

| 入口 | 用途 |
|---|---|
| teleop/panda.py、configs/panda_model.json | Panda 关节与夹爪适配 |
| teleop/assets/franka_emika_panda/ | 上游公开模型、网格与来源许可 |
| teleop/manual.py、teleop/web/ | 浏览器交互、服务与记录 |
| tests/test_panda.py | 4 项新增测试，与 2 项回归测试合计增加至 29 项 |
| reports/RESULTS_V02.md 等 | 当前模型、UI、通信与打包验证 |
| manual_demo_episode/ | 与视频/PPT 对应的自动 UI 仿真数据 |
| defense/ | PPT、视频、讲稿、操作卡、预览、截图、字体与制作来源 |
| examples/ui_browser_validation.mjs 等 | 可选自动浏览器流程检查 |
| requirements-tested.txt、MANIFEST.sha256 | 核心依赖记录与文件校验 |

## 两版都尚未完成的目标

实体 GELLO/Franka/UR 接入、实机动力学对齐、厂家实时伺服、实体停止与使能、相机同步、异构 IK、力反馈、跨地域实验、任务成功自动标注、学习格式转换与训练均未完成。

不同模型、不同运行中的 Hz、确认延迟和 RMSE，不能直接作为两版算法优劣的对照证据。

## 本次团队文档更新（软件仍为 0.2.0）

新增总指南、版本对照、全部文件索引和 GitHub 步骤；重写任务表并为 README 加入口；修正 v0.2 报告中未展开的数组形状为 `(3517, 7)`，补充 Panda 夹爪数据语义。

没有改运行代码、配置、依赖、测试代码、PPT、视频和原始 episode。原实验数字保持不变。本次检查文档链接、文件索引、命令入口和样例完整性，不声称重做了所有实验。
