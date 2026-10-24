# 全部材料索引 · v0.3

普通组员先看 [零基础指南](TEAM_GUIDE.md)，不用按下表逐个读代码。完整逐文件审查方法见 [FILE_AUDIT.md](../reports/FILE_AUDIT.md)。

下表只列交付文件；个人环境、运行目录、缓存和构建中间物不随包发送。

## 项目元文件

| 文件 | 用途/检查 |
|---|---|
| [.gitignore](../.gitignore) | 用途与完整性核对 |
| [MANIFEST.sha256](../MANIFEST.sha256) | 用途与完整性核对 |
| [examples/calibration_pairs.json](../examples/calibration_pairs.json) | 用途与完整性核对 |
| [examples/package.json](../examples/package.json) | 用途与完整性核对 |
| [pyproject.toml](../pyproject.toml) | 用途与完整性核对 |
| [requirements-tested.txt](../requirements-tested.txt) | 用途与完整性核对 |
| [teleop/web/SOURCE.json](../teleop/web/SOURCE.json) | 用途与完整性核对 |
| [teleop/web/THREE_LICENSE.txt](../teleop/web/THREE_LICENSE.txt) | 用途与完整性核对 |

## 说明材料

| 文件 | 用途/检查 |
|---|---|
| [README.md](../README.md) | 操作、术语、来源及版本口径核对 |
| [START_HERE.html](../START_HERE.html) | 操作、术语、来源及版本口径核对 |
| [defense/defense-operation-card.md](../defense/defense-operation-card.md) | 操作、术语、来源及版本口径核对 |
| [defense/defense-script-and-qa.md](../defense/defense-script-and-qa.md) | 操作、术语、来源及版本口径核对 |
| [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) | 操作、术语、来源及版本口径核对 |
| [docs/DATA_SCHEMA.md](../docs/DATA_SCHEMA.md) | 操作、术语、来源及版本口径核对 |
| [docs/GITHUB_UPDATE.md](../docs/GITHUB_UPDATE.md) | 操作、术语、来源及版本口径核对 |
| [docs/HARDWARE.md](../docs/HARDWARE.md) | 操作、术语、来源及版本口径核对 |
| [docs/MANUAL_UI.md](../docs/MANUAL_UI.md) | 操作、术语、来源及版本口径核对 |
| [docs/MATERIAL_INDEX.md](../docs/MATERIAL_INDEX.md) | 操作、术语、来源及版本口径核对 |
| [docs/ON_SITE_ONLY.md](../docs/ON_SITE_ONLY.md) | 操作、术语、来源及版本口径核对 |
| [docs/SOURCES.md](../docs/SOURCES.md) | 操作、术语、来源及版本口径核对 |
| [docs/TEAM_GUIDE.md](../docs/TEAM_GUIDE.md) | 操作、术语、来源及版本口径核对 |
| [docs/TEAM_TASKS.md](../docs/TEAM_TASKS.md) | 操作、术语、来源及版本口径核对 |
| [docs/VERSION_COMPARISON.md](../docs/VERSION_COMPARISON.md) | 操作、术语、来源及版本口径核对 |
| [examples/README_UI_CHECK.md](../examples/README_UI_CHECK.md) | 操作、术语、来源及版本口径核对 |
| [teleop/web/index.html](../teleop/web/index.html) | 操作、术语、来源及版本口径核对 |

## 第一方代码/入口

| 文件 | 用途/检查 |
|---|---|
| [START.bat](../START.bat) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [START.command](../START.command) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [START.sh](../START.sh) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [examples/loopback_validation.py](../examples/loopback_validation.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [examples/plot_results.py](../examples/plot_results.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [examples/ui_browser_validation.mjs](../examples/ui_browser_validation.mjs) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [examples/validate.py](../examples/validate.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [run.py](../run.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/__init__.py](../teleop/__init__.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/__main__.py](../teleop/__main__.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/cli.py](../teleop/cli.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/config.py](../teleop/config.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/control.py](../teleop/control.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/diagnostics.py](../teleop/diagnostics.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/manual.py](../teleop/manual.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/mapping.py](../teleop/mapping.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/network.py](../teleop/network.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/panda.py](../teleop/panda.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/protocol.py](../teleop/protocol.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/quality.py](../teleop/quality.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/recording.py](../teleop/recording.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/robot.py](../teleop/robot.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/simulation.py](../teleop/simulation.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/web/app.js](../teleop/web/app.js) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/web/control-worker.js](../teleop/web/control-worker.js) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [tests/test_audit_regressions.py](../tests/test_audit_regressions.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [tests/test_core.py](../tests/test_core.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [tests/test_network.py](../tests/test_network.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [tests/test_panda.py](../tests/test_panda.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [tools/run_tests.py](../tools/run_tests.py) | 源码审查；相关测试/流程验证；平台边界见报告 |
| [tools/verify_package.py](../tools/verify_package.py) | 源码审查；相关测试/流程验证；平台边界见报告 |

## 配置

| 文件 | 用途/检查 |
|---|---|
| [configs/gello.example.json](../configs/gello.example.json) | 维数、范围、占位值与对应用途核对 |
| [configs/panda7_sim.json](../configs/panda7_sim.json) | 维数、范围、占位值与对应用途核对 |
| [configs/panda_model.json](../configs/panda_model.json) | 维数、范围、占位值与对应用途核对 |
| [configs/ur6_sim.json](../configs/ur6_sim.json) | 维数、范围、占位值与对应用途核对 |

## 历史演示媒体

| 文件 | 用途/检查 |
|---|---|
| [defense/evidence/demo-active.png](../defense/evidence/demo-active.png) | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo-checks.json](../defense/evidence/demo-checks.json) | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo-estop.png](../defense/evidence/demo-estop.png) | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo-gripper.png](../defense/evidence/demo-gripper.png) | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo-hold.png](../defense/evidence/demo-hold.png) | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo-marks.json](../defense/evidence/demo-marks.json) | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo-saved.png](../defense/evidence/demo-saved.png) | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo.srt](../defense/evidence/demo.srt) | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/evidence.json](../defense/evidence/evidence.json) | 来源、完整性、媒体信息与样例对应 |
| [defense/panda-teleop-demo.mp4](../defense/panda-teleop-demo.mp4) | 来源、完整性、媒体信息与样例对应 |

## 第三方资源

| 文件 | 用途/检查 |
|---|---|
| [defense/fonts/LICENSE.txt](../defense/fonts/LICENSE.txt) | 来源/许可与完整性；按用途模型/网页加载 |
| [defense/fonts/NotoSansCJKsc-Regular.otf](../defense/fonts/NotoSansCJKsc-Regular.otf) | 来源/许可与完整性；按用途模型/网页加载 |
| [defense/fonts/SOURCE.json](../defense/fonts/SOURCE.json) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/CHANGELOG.md](../teleop/assets/franka_emika_panda/CHANGELOG.md) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/LICENSE](../teleop/assets/franka_emika_panda/LICENSE) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/README.md](../teleop/assets/franka_emika_panda/README.md) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/SOURCE.json](../teleop/assets/franka_emika_panda/SOURCE.json) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/finger_0.obj](../teleop/assets/franka_emika_panda/assets/finger_0.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/finger_1.obj](../teleop/assets/franka_emika_panda/assets/finger_1.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/hand.stl](../teleop/assets/franka_emika_panda/assets/hand.stl) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/hand_0.obj](../teleop/assets/franka_emika_panda/assets/hand_0.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/hand_1.obj](../teleop/assets/franka_emika_panda/assets/hand_1.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/hand_2.obj](../teleop/assets/franka_emika_panda/assets/hand_2.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/hand_3.obj](../teleop/assets/franka_emika_panda/assets/hand_3.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/hand_4.obj](../teleop/assets/franka_emika_panda/assets/hand_4.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0.stl](../teleop/assets/franka_emika_panda/assets/link0.stl) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_0.obj](../teleop/assets/franka_emika_panda/assets/link0_0.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_1.obj](../teleop/assets/franka_emika_panda/assets/link0_1.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_10.obj](../teleop/assets/franka_emika_panda/assets/link0_10.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_11.obj](../teleop/assets/franka_emika_panda/assets/link0_11.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_2.obj](../teleop/assets/franka_emika_panda/assets/link0_2.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_3.obj](../teleop/assets/franka_emika_panda/assets/link0_3.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_4.obj](../teleop/assets/franka_emika_panda/assets/link0_4.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_5.obj](../teleop/assets/franka_emika_panda/assets/link0_5.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_7.obj](../teleop/assets/franka_emika_panda/assets/link0_7.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_8.obj](../teleop/assets/franka_emika_panda/assets/link0_8.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_9.obj](../teleop/assets/franka_emika_panda/assets/link0_9.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link1.obj](../teleop/assets/franka_emika_panda/assets/link1.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link1.stl](../teleop/assets/franka_emika_panda/assets/link1.stl) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link2.obj](../teleop/assets/franka_emika_panda/assets/link2.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link2.stl](../teleop/assets/franka_emika_panda/assets/link2.stl) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link3.stl](../teleop/assets/franka_emika_panda/assets/link3.stl) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link3_0.obj](../teleop/assets/franka_emika_panda/assets/link3_0.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link3_1.obj](../teleop/assets/franka_emika_panda/assets/link3_1.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link3_2.obj](../teleop/assets/franka_emika_panda/assets/link3_2.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link3_3.obj](../teleop/assets/franka_emika_panda/assets/link3_3.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link4.stl](../teleop/assets/franka_emika_panda/assets/link4.stl) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link4_0.obj](../teleop/assets/franka_emika_panda/assets/link4_0.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link4_1.obj](../teleop/assets/franka_emika_panda/assets/link4_1.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link4_2.obj](../teleop/assets/franka_emika_panda/assets/link4_2.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link4_3.obj](../teleop/assets/franka_emika_panda/assets/link4_3.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link5_0.obj](../teleop/assets/franka_emika_panda/assets/link5_0.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link5_1.obj](../teleop/assets/franka_emika_panda/assets/link5_1.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link5_2.obj](../teleop/assets/franka_emika_panda/assets/link5_2.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link5_collision_0.obj](../teleop/assets/franka_emika_panda/assets/link5_collision_0.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link5_collision_1.obj](../teleop/assets/franka_emika_panda/assets/link5_collision_1.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link5_collision_2.obj](../teleop/assets/franka_emika_panda/assets/link5_collision_2.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6.stl](../teleop/assets/franka_emika_panda/assets/link6.stl) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_0.obj](../teleop/assets/franka_emika_panda/assets/link6_0.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_1.obj](../teleop/assets/franka_emika_panda/assets/link6_1.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_10.obj](../teleop/assets/franka_emika_panda/assets/link6_10.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_11.obj](../teleop/assets/franka_emika_panda/assets/link6_11.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_12.obj](../teleop/assets/franka_emika_panda/assets/link6_12.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_13.obj](../teleop/assets/franka_emika_panda/assets/link6_13.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_14.obj](../teleop/assets/franka_emika_panda/assets/link6_14.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_15.obj](../teleop/assets/franka_emika_panda/assets/link6_15.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_16.obj](../teleop/assets/franka_emika_panda/assets/link6_16.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_2.obj](../teleop/assets/franka_emika_panda/assets/link6_2.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_3.obj](../teleop/assets/franka_emika_panda/assets/link6_3.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_4.obj](../teleop/assets/franka_emika_panda/assets/link6_4.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_5.obj](../teleop/assets/franka_emika_panda/assets/link6_5.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_6.obj](../teleop/assets/franka_emika_panda/assets/link6_6.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_7.obj](../teleop/assets/franka_emika_panda/assets/link6_7.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_8.obj](../teleop/assets/franka_emika_panda/assets/link6_8.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_9.obj](../teleop/assets/franka_emika_panda/assets/link6_9.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7.stl](../teleop/assets/franka_emika_panda/assets/link7.stl) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_0.obj](../teleop/assets/franka_emika_panda/assets/link7_0.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_1.obj](../teleop/assets/franka_emika_panda/assets/link7_1.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_2.obj](../teleop/assets/franka_emika_panda/assets/link7_2.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_3.obj](../teleop/assets/franka_emika_panda/assets/link7_3.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_4.obj](../teleop/assets/franka_emika_panda/assets/link7_4.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_5.obj](../teleop/assets/franka_emika_panda/assets/link7_5.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_6.obj](../teleop/assets/franka_emika_panda/assets/link7_6.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_7.obj](../teleop/assets/franka_emika_panda/assets/link7_7.obj) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/panda.xml](../teleop/assets/franka_emika_panda/panda.xml) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/scene.xml](../teleop/assets/franka_emika_panda/scene.xml) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/web/OrbitControls.js](../teleop/web/OrbitControls.js) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/web/three.core.js](../teleop/web/three.core.js) | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/web/three.module.js](../teleop/web/three.module.js) | 来源/许可与完整性；按用途模型/网页加载 |

## 答辩幻灯片

| 文件 | 用途/检查 |
|---|---|
| [defense/robot-teleop-defense.pptx](../defense/robot-teleop-defense.pptx) | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-01.png](../defense/slide-previews/slide-01.png) | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-02.png](../defense/slide-previews/slide-02.png) | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-03.png](../defense/slide-previews/slide-03.png) | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-04.png](../defense/slide-previews/slide-04.png) | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-05.png](../defense/slide-previews/slide-05.png) | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-06.png](../defense/slide-previews/slide-06.png) | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-07.png](../defense/slide-previews/slide-07.png) | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-08.png](../defense/slide-previews/slide-08.png) | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-09.png](../defense/slide-previews/slide-09.png) | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-10.png](../defense/slide-previews/slide-10.png) | 文字/数字、包结构、渲染逐页检查 |

## 材料制作来源

| 文件 | 用途/检查 |
|---|---|
| [defense/source/README.md](../defense/source/README.md) | 制作路径与依赖说明；非用户启动入口 |
| [defense/source/build-defense.mjs](../defense/source/build-defense.mjs) | 制作路径与依赖说明；非用户启动入口 |
| [defense/source/recording-run.mjs](../defense/source/recording-run.mjs) | 制作路径与依赖说明；非用户启动入口 |
| [defense/source/restore_chart.py](../defense/source/restore_chart.py) | 制作路径与依赖说明；非用户启动入口 |
| [defense/source/update-v03.mjs](../defense/source/update-v03.mjs) | 制作路径与依赖说明；非用户启动入口 |

## 历史说明

| 文件 | 用途/检查 |
|---|---|
| [docs/history/README_V02.md](../docs/history/README_V02.md) | 来源保留；旧操作不作为当前入口 |
| [docs/history/TEAM_GUIDE_V02.md](../docs/history/TEAM_GUIDE_V02.md) | 来源保留；旧操作不作为当前入口 |

## 历史证据

| 文件 | 用途/检查 |
|---|---|
| [manual_demo_episode/episode.npz](../manual_demo_episode/episode.npz) | 完整性/数据检查；历史结论边界核对 |
| [manual_demo_episode/metadata.json](../manual_demo_episode/metadata.json) | 完整性/数据检查；历史结论边界核对 |
| [manual_demo_episode/steps.jsonl](../manual_demo_episode/steps.jsonl) | 完整性/数据检查；历史结论边界核对 |
| [manual_demo_episode/summary.json](../manual_demo_episode/summary.json) | 完整性/数据检查；历史结论边界核对 |
| [reports/RESULTS.md](../reports/RESULTS.md) | 完整性/数据检查；历史结论边界核对 |
| [reports/RESULTS_V02.md](../reports/RESULTS_V02.md) | 完整性/数据检查；历史结论边界核对 |
| [reports/loopback.json](../reports/loopback.json) | 完整性/数据检查；历史结论边界核对 |
| [reports/manual-demo.json](../reports/manual-demo.json) | 完整性/数据检查；历史结论边界核对 |
| [reports/packaging-check.json](../reports/packaging-check.json) | 完整性/数据检查；历史结论边界核对 |
| [reports/panda-loopback-load-fault.json](../reports/panda-loopback-load-fault.json) | 完整性/数据检查；历史结论边界核对 |
| [reports/panda-loopback.json](../reports/panda-loopback.json) | 完整性/数据检查；历史结论边界核对 |
| [reports/tests-v02.txt](../reports/tests-v02.txt) | 完整性/数据检查；历史结论边界核对 |
| [reports/tests.txt](../reports/tests.txt) | 完整性/数据检查；历史结论边界核对 |
| [reports/ui-checks.json](../reports/ui-checks.json) | 完整性/数据检查；历史结论边界核对 |
| [reports/validation.json](../reports/validation.json) | 完整性/数据检查；历史结论边界核对 |
| [reports/validation.png](../reports/validation.png) | 完整性/数据检查；历史结论边界核对 |
| [sample_episode/metadata.json](../sample_episode/metadata.json) | 完整性/数据检查；历史结论边界核对 |
| [sample_episode/steps.jsonl](../sample_episode/steps.jsonl) | 完整性/数据检查；历史结论边界核对 |
| [sample_episode/summary.json](../sample_episode/summary.json) | 完整性/数据检查；历史结论边界核对 |
| [sample_episode.npz](../sample_episode.npz) | 完整性/数据检查；历史结论边界核对 |

## v0.3 证据

| 文件 | 用途/检查 |
|---|---|
| [reports/AUDIT_V03.md](../reports/AUDIT_V03.md) | 本次生成；结果与原始输出核对 |
| [reports/FILE_AUDIT.md](../reports/FILE_AUDIT.md) | 本次生成；结果与原始输出核对 |
| [reports/v03/browser-check.json](../reports/v03/browser-check.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/github-access.json](../reports/v03/github-access.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/guide-check.json](../reports/v03/guide-check.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/historical-quality.json](../reports/v03/historical-quality.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/launcher-check.json](../reports/v03/launcher-check.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/environment.json](../reports/v03/self-check/environment.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/panda-episode/episode.npz](../reports/v03/self-check/panda-episode/episode.npz) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/panda-episode/metadata.json](../reports/v03/self-check/panda-episode/metadata.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/panda-episode/quality-report/report.html](../reports/v03/self-check/panda-episode/quality-report/report.html) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/panda-episode/quality-report/report.json](../reports/v03/self-check/panda-episode/quality-report/report.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/panda-episode/steps.jsonl](../reports/v03/self-check/panda-episode/steps.jsonl) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/panda-episode/summary.json](../reports/v03/self-check/panda-episode/summary.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/report.html](../reports/v03/self-check/report.html) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/report.json](../reports/v03/self-check/report.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/test-runner.log](../reports/v03/self-check/test-runner.log) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/tests/tests.json](../reports/v03/self-check/tests/tests.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/tests/tests.log](../reports/v03/self-check/tests/tests.log) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/udp/episode/metadata.json](../reports/v03/self-check/udp/episode/metadata.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/udp/episode/steps.jsonl](../reports/v03/self-check/udp/episode/steps.jsonl) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/udp/episode/summary.json](../reports/v03/self-check/udp/episode/summary.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/udp/loopback.json](../reports/v03/self-check/udp/loopback.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/udp.log](../reports/v03/self-check/udp.log) | 本次生成；结果与原始输出核对 |
| [reports/v03/tests/tests.json](../reports/v03/tests/tests.json) | 本次生成；结果与原始输出核对 |
| [reports/v03/tests/tests.log](../reports/v03/tests/tests.log) | 本次生成；结果与原始输出核对 |
| [reports/v03/ui-active.png](../reports/v03/ui-active.png) | 本次生成；结果与原始输出核对 |
| [reports/v03/ui-save-failure.png](../reports/v03/ui-save-failure.png) | 本次生成；结果与原始输出核对 |
| [reports/v03/ui-saved.png](../reports/v03/ui-saved.png) | 本次生成；结果与原始输出核对 |
| [reports/v03/wheel-check.json](../reports/v03/wheel-check.json) | 本次生成；结果与原始输出核对 |
