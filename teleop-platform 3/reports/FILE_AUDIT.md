# 逐文件审查登记 · v0.3

交付清单共 217 个文件。对照基线是 172 文件 v0.2 团队工程；不是尚无法访问的 GitHub 最新提交。

“检查方法”按文件性质区分。第三方模型/字体/库只做来源、完整性与加载核对，不宣称逐行安全审计；macOS/Windows 启动文件只做结构核对，未原生实测。当前详细结果见 [审查报告](AUDIT_V03.md)。

| 文件 | 相对上一交付 | 类别 | 检查方法 |
|---|---|---|---|
| [.gitignore](../.gitignore) | 修改 | 项目元文件 | 用途与完整性核对 |
| [MANIFEST.sha256](../MANIFEST.sha256) | 重新生成 | 项目元文件 | 用途与完整性核对 |
| [README.md](../README.md) | 修改 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [START.bat](../START.bat) | 新增 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [START.command](../START.command) | 新增 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [START.sh](../START.sh) | 新增 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [START_HERE.html](../START_HERE.html) | 新增 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [configs/gello.example.json](../configs/gello.example.json) | 保留 | 配置 | 维数、范围、占位值与对应用途核对 |
| [configs/panda7_sim.json](../configs/panda7_sim.json) | 保留 | 配置 | 维数、范围、占位值与对应用途核对 |
| [configs/panda_model.json](../configs/panda_model.json) | 保留 | 配置 | 维数、范围、占位值与对应用途核对 |
| [configs/ur6_sim.json](../configs/ur6_sim.json) | 保留 | 配置 | 维数、范围、占位值与对应用途核对 |
| [defense/defense-operation-card.md](../defense/defense-operation-card.md) | 修改 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [defense/defense-script-and-qa.md](../defense/defense-script-and-qa.md) | 修改 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [defense/evidence/demo-active.png](../defense/evidence/demo-active.png) | 保留 | 历史演示媒体 | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo-checks.json](../defense/evidence/demo-checks.json) | 保留 | 历史演示媒体 | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo-estop.png](../defense/evidence/demo-estop.png) | 保留 | 历史演示媒体 | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo-gripper.png](../defense/evidence/demo-gripper.png) | 保留 | 历史演示媒体 | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo-hold.png](../defense/evidence/demo-hold.png) | 保留 | 历史演示媒体 | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo-marks.json](../defense/evidence/demo-marks.json) | 保留 | 历史演示媒体 | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo-saved.png](../defense/evidence/demo-saved.png) | 保留 | 历史演示媒体 | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/demo.srt](../defense/evidence/demo.srt) | 保留 | 历史演示媒体 | 来源、完整性、媒体信息与样例对应 |
| [defense/evidence/evidence.json](../defense/evidence/evidence.json) | 保留 | 历史演示媒体 | 来源、完整性、媒体信息与样例对应 |
| [defense/fonts/LICENSE.txt](../defense/fonts/LICENSE.txt) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [defense/fonts/NotoSansCJKsc-Regular.otf](../defense/fonts/NotoSansCJKsc-Regular.otf) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [defense/fonts/SOURCE.json](../defense/fonts/SOURCE.json) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [defense/panda-teleop-demo.mp4](../defense/panda-teleop-demo.mp4) | 保留 | 历史演示媒体 | 来源、完整性、媒体信息与样例对应 |
| [defense/robot-teleop-defense.pptx](../defense/robot-teleop-defense.pptx) | 修改 | 答辩幻灯片 | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-01.png](../defense/slide-previews/slide-01.png) | 修改 | 答辩幻灯片 | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-02.png](../defense/slide-previews/slide-02.png) | 修改 | 答辩幻灯片 | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-03.png](../defense/slide-previews/slide-03.png) | 修改 | 答辩幻灯片 | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-04.png](../defense/slide-previews/slide-04.png) | 修改 | 答辩幻灯片 | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-05.png](../defense/slide-previews/slide-05.png) | 修改 | 答辩幻灯片 | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-06.png](../defense/slide-previews/slide-06.png) | 修改 | 答辩幻灯片 | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-07.png](../defense/slide-previews/slide-07.png) | 修改 | 答辩幻灯片 | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-08.png](../defense/slide-previews/slide-08.png) | 修改 | 答辩幻灯片 | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-09.png](../defense/slide-previews/slide-09.png) | 修改 | 答辩幻灯片 | 文字/数字、包结构、渲染逐页检查 |
| [defense/slide-previews/slide-10.png](../defense/slide-previews/slide-10.png) | 修改 | 答辩幻灯片 | 文字/数字、包结构、渲染逐页检查 |
| [defense/source/README.md](../defense/source/README.md) | 修改 | 材料制作来源 | 制作路径与依赖说明；非用户启动入口 |
| [defense/source/build-defense.mjs](../defense/source/build-defense.mjs) | 保留 | 材料制作来源 | 制作路径与依赖说明；非用户启动入口 |
| [defense/source/recording-run.mjs](../defense/source/recording-run.mjs) | 保留 | 材料制作来源 | 制作路径与依赖说明；非用户启动入口 |
| [defense/source/restore_chart.py](../defense/source/restore_chart.py) | 新增 | 材料制作来源 | 制作路径与依赖说明；非用户启动入口 |
| [defense/source/update-v03.mjs](../defense/source/update-v03.mjs) | 新增 | 材料制作来源 | 制作路径与依赖说明；非用户启动入口 |
| [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) | 修改 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [docs/DATA_SCHEMA.md](../docs/DATA_SCHEMA.md) | 修改 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [docs/GITHUB_UPDATE.md](../docs/GITHUB_UPDATE.md) | 修改 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [docs/HARDWARE.md](../docs/HARDWARE.md) | 保留 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [docs/MANUAL_UI.md](../docs/MANUAL_UI.md) | 修改 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [docs/MATERIAL_INDEX.md](../docs/MATERIAL_INDEX.md) | 修改 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [docs/ON_SITE_ONLY.md](../docs/ON_SITE_ONLY.md) | 新增 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [docs/SOURCES.md](../docs/SOURCES.md) | 保留 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [docs/TEAM_GUIDE.md](../docs/TEAM_GUIDE.md) | 修改 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [docs/TEAM_TASKS.md](../docs/TEAM_TASKS.md) | 修改 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [docs/VERSION_COMPARISON.md](../docs/VERSION_COMPARISON.md) | 修改 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [docs/history/README_V02.md](../docs/history/README_V02.md) | 新增 | 历史说明 | 来源保留；旧操作不作为当前入口 |
| [docs/history/TEAM_GUIDE_V02.md](../docs/history/TEAM_GUIDE_V02.md) | 新增 | 历史说明 | 来源保留；旧操作不作为当前入口 |
| [examples/README_UI_CHECK.md](../examples/README_UI_CHECK.md) | 修改 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [examples/calibration_pairs.json](../examples/calibration_pairs.json) | 保留 | 项目元文件 | 用途与完整性核对 |
| [examples/loopback_validation.py](../examples/loopback_validation.py) | 保留 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [examples/package.json](../examples/package.json) | 保留 | 项目元文件 | 用途与完整性核对 |
| [examples/plot_results.py](../examples/plot_results.py) | 保留 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [examples/ui_browser_validation.mjs](../examples/ui_browser_validation.mjs) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [examples/validate.py](../examples/validate.py) | 保留 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [manual_demo_episode/episode.npz](../manual_demo_episode/episode.npz) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [manual_demo_episode/metadata.json](../manual_demo_episode/metadata.json) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [manual_demo_episode/steps.jsonl](../manual_demo_episode/steps.jsonl) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [manual_demo_episode/summary.json](../manual_demo_episode/summary.json) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [pyproject.toml](../pyproject.toml) | 修改 | 项目元文件 | 用途与完整性核对 |
| [reports/AUDIT_V03.md](../reports/AUDIT_V03.md) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/FILE_AUDIT.md](../reports/FILE_AUDIT.md) | 重新生成 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/RESULTS.md](../reports/RESULTS.md) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [reports/RESULTS_V02.md](../reports/RESULTS_V02.md) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [reports/loopback.json](../reports/loopback.json) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [reports/manual-demo.json](../reports/manual-demo.json) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [reports/packaging-check.json](../reports/packaging-check.json) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [reports/panda-loopback-load-fault.json](../reports/panda-loopback-load-fault.json) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [reports/panda-loopback.json](../reports/panda-loopback.json) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [reports/tests-v02.txt](../reports/tests-v02.txt) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [reports/tests.txt](../reports/tests.txt) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [reports/ui-checks.json](../reports/ui-checks.json) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [reports/v03/browser-check.json](../reports/v03/browser-check.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/github-access.json](../reports/v03/github-access.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/guide-check.json](../reports/v03/guide-check.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/historical-quality.json](../reports/v03/historical-quality.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/launcher-check.json](../reports/v03/launcher-check.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/environment.json](../reports/v03/self-check/environment.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/panda-episode/episode.npz](../reports/v03/self-check/panda-episode/episode.npz) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/panda-episode/metadata.json](../reports/v03/self-check/panda-episode/metadata.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/panda-episode/quality-report/report.html](../reports/v03/self-check/panda-episode/quality-report/report.html) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/panda-episode/quality-report/report.json](../reports/v03/self-check/panda-episode/quality-report/report.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/panda-episode/steps.jsonl](../reports/v03/self-check/panda-episode/steps.jsonl) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/panda-episode/summary.json](../reports/v03/self-check/panda-episode/summary.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/report.html](../reports/v03/self-check/report.html) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/report.json](../reports/v03/self-check/report.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/test-runner.log](../reports/v03/self-check/test-runner.log) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/tests/tests.json](../reports/v03/self-check/tests/tests.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/tests/tests.log](../reports/v03/self-check/tests/tests.log) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/udp/episode/metadata.json](../reports/v03/self-check/udp/episode/metadata.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/udp/episode/steps.jsonl](../reports/v03/self-check/udp/episode/steps.jsonl) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/udp/episode/summary.json](../reports/v03/self-check/udp/episode/summary.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/udp/loopback.json](../reports/v03/self-check/udp/loopback.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/self-check/udp.log](../reports/v03/self-check/udp.log) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/tests/tests.json](../reports/v03/tests/tests.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/tests/tests.log](../reports/v03/tests/tests.log) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/ui-active.png](../reports/v03/ui-active.png) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/ui-save-failure.png](../reports/v03/ui-save-failure.png) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/ui-saved.png](../reports/v03/ui-saved.png) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/v03/wheel-check.json](../reports/v03/wheel-check.json) | 新增 | v0.3 证据 | 本次生成；结果与原始输出核对 |
| [reports/validation.json](../reports/validation.json) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [reports/validation.png](../reports/validation.png) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [requirements-tested.txt](../requirements-tested.txt) | 修改 | 项目元文件 | 用途与完整性核对 |
| [run.py](../run.py) | 新增 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [sample_episode/metadata.json](../sample_episode/metadata.json) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [sample_episode/steps.jsonl](../sample_episode/steps.jsonl) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [sample_episode/summary.json](../sample_episode/summary.json) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [sample_episode.npz](../sample_episode.npz) | 保留 | 历史证据 | 完整性/数据检查；历史结论边界核对 |
| [teleop/__init__.py](../teleop/__init__.py) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/__main__.py](../teleop/__main__.py) | 保留 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/assets/franka_emika_panda/CHANGELOG.md](../teleop/assets/franka_emika_panda/CHANGELOG.md) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/LICENSE](../teleop/assets/franka_emika_panda/LICENSE) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/README.md](../teleop/assets/franka_emika_panda/README.md) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/SOURCE.json](../teleop/assets/franka_emika_panda/SOURCE.json) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/finger_0.obj](../teleop/assets/franka_emika_panda/assets/finger_0.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/finger_1.obj](../teleop/assets/franka_emika_panda/assets/finger_1.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/hand.stl](../teleop/assets/franka_emika_panda/assets/hand.stl) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/hand_0.obj](../teleop/assets/franka_emika_panda/assets/hand_0.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/hand_1.obj](../teleop/assets/franka_emika_panda/assets/hand_1.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/hand_2.obj](../teleop/assets/franka_emika_panda/assets/hand_2.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/hand_3.obj](../teleop/assets/franka_emika_panda/assets/hand_3.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/hand_4.obj](../teleop/assets/franka_emika_panda/assets/hand_4.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0.stl](../teleop/assets/franka_emika_panda/assets/link0.stl) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_0.obj](../teleop/assets/franka_emika_panda/assets/link0_0.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_1.obj](../teleop/assets/franka_emika_panda/assets/link0_1.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_10.obj](../teleop/assets/franka_emika_panda/assets/link0_10.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_11.obj](../teleop/assets/franka_emika_panda/assets/link0_11.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_2.obj](../teleop/assets/franka_emika_panda/assets/link0_2.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_3.obj](../teleop/assets/franka_emika_panda/assets/link0_3.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_4.obj](../teleop/assets/franka_emika_panda/assets/link0_4.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_5.obj](../teleop/assets/franka_emika_panda/assets/link0_5.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_7.obj](../teleop/assets/franka_emika_panda/assets/link0_7.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_8.obj](../teleop/assets/franka_emika_panda/assets/link0_8.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link0_9.obj](../teleop/assets/franka_emika_panda/assets/link0_9.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link1.obj](../teleop/assets/franka_emika_panda/assets/link1.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link1.stl](../teleop/assets/franka_emika_panda/assets/link1.stl) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link2.obj](../teleop/assets/franka_emika_panda/assets/link2.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link2.stl](../teleop/assets/franka_emika_panda/assets/link2.stl) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link3.stl](../teleop/assets/franka_emika_panda/assets/link3.stl) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link3_0.obj](../teleop/assets/franka_emika_panda/assets/link3_0.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link3_1.obj](../teleop/assets/franka_emika_panda/assets/link3_1.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link3_2.obj](../teleop/assets/franka_emika_panda/assets/link3_2.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link3_3.obj](../teleop/assets/franka_emika_panda/assets/link3_3.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link4.stl](../teleop/assets/franka_emika_panda/assets/link4.stl) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link4_0.obj](../teleop/assets/franka_emika_panda/assets/link4_0.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link4_1.obj](../teleop/assets/franka_emika_panda/assets/link4_1.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link4_2.obj](../teleop/assets/franka_emika_panda/assets/link4_2.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link4_3.obj](../teleop/assets/franka_emika_panda/assets/link4_3.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link5_0.obj](../teleop/assets/franka_emika_panda/assets/link5_0.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link5_1.obj](../teleop/assets/franka_emika_panda/assets/link5_1.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link5_2.obj](../teleop/assets/franka_emika_panda/assets/link5_2.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link5_collision_0.obj](../teleop/assets/franka_emika_panda/assets/link5_collision_0.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link5_collision_1.obj](../teleop/assets/franka_emika_panda/assets/link5_collision_1.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link5_collision_2.obj](../teleop/assets/franka_emika_panda/assets/link5_collision_2.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6.stl](../teleop/assets/franka_emika_panda/assets/link6.stl) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_0.obj](../teleop/assets/franka_emika_panda/assets/link6_0.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_1.obj](../teleop/assets/franka_emika_panda/assets/link6_1.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_10.obj](../teleop/assets/franka_emika_panda/assets/link6_10.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_11.obj](../teleop/assets/franka_emika_panda/assets/link6_11.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_12.obj](../teleop/assets/franka_emika_panda/assets/link6_12.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_13.obj](../teleop/assets/franka_emika_panda/assets/link6_13.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_14.obj](../teleop/assets/franka_emika_panda/assets/link6_14.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_15.obj](../teleop/assets/franka_emika_panda/assets/link6_15.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_16.obj](../teleop/assets/franka_emika_panda/assets/link6_16.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_2.obj](../teleop/assets/franka_emika_panda/assets/link6_2.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_3.obj](../teleop/assets/franka_emika_panda/assets/link6_3.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_4.obj](../teleop/assets/franka_emika_panda/assets/link6_4.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_5.obj](../teleop/assets/franka_emika_panda/assets/link6_5.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_6.obj](../teleop/assets/franka_emika_panda/assets/link6_6.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_7.obj](../teleop/assets/franka_emika_panda/assets/link6_7.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_8.obj](../teleop/assets/franka_emika_panda/assets/link6_8.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link6_9.obj](../teleop/assets/franka_emika_panda/assets/link6_9.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7.stl](../teleop/assets/franka_emika_panda/assets/link7.stl) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_0.obj](../teleop/assets/franka_emika_panda/assets/link7_0.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_1.obj](../teleop/assets/franka_emika_panda/assets/link7_1.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_2.obj](../teleop/assets/franka_emika_panda/assets/link7_2.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_3.obj](../teleop/assets/franka_emika_panda/assets/link7_3.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_4.obj](../teleop/assets/franka_emika_panda/assets/link7_4.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_5.obj](../teleop/assets/franka_emika_panda/assets/link7_5.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_6.obj](../teleop/assets/franka_emika_panda/assets/link7_6.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/assets/link7_7.obj](../teleop/assets/franka_emika_panda/assets/link7_7.obj) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/panda.xml](../teleop/assets/franka_emika_panda/panda.xml) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/assets/franka_emika_panda/scene.xml](../teleop/assets/franka_emika_panda/scene.xml) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/cli.py](../teleop/cli.py) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/config.py](../teleop/config.py) | 保留 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/control.py](../teleop/control.py) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/diagnostics.py](../teleop/diagnostics.py) | 新增 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/manual.py](../teleop/manual.py) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/mapping.py](../teleop/mapping.py) | 保留 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/network.py](../teleop/network.py) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/panda.py](../teleop/panda.py) | 保留 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/protocol.py](../teleop/protocol.py) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/quality.py](../teleop/quality.py) | 新增 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/recording.py](../teleop/recording.py) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/robot.py](../teleop/robot.py) | 保留 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/simulation.py](../teleop/simulation.py) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/web/OrbitControls.js](../teleop/web/OrbitControls.js) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/web/SOURCE.json](../teleop/web/SOURCE.json) | 保留 | 项目元文件 | 用途与完整性核对 |
| [teleop/web/THREE_LICENSE.txt](../teleop/web/THREE_LICENSE.txt) | 保留 | 项目元文件 | 用途与完整性核对 |
| [teleop/web/app.js](../teleop/web/app.js) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/web/control-worker.js](../teleop/web/control-worker.js) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [teleop/web/index.html](../teleop/web/index.html) | 保留 | 说明材料 | 操作、术语、来源及版本口径核对 |
| [teleop/web/three.core.js](../teleop/web/three.core.js) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [teleop/web/three.module.js](../teleop/web/three.module.js) | 保留 | 第三方资源 | 来源/许可与完整性；按用途模型/网页加载 |
| [tests/test_audit_regressions.py](../tests/test_audit_regressions.py) | 新增 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [tests/test_core.py](../tests/test_core.py) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [tests/test_network.py](../tests/test_network.py) | 保留 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [tests/test_panda.py](../tests/test_panda.py) | 修改 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [tools/run_tests.py](../tools/run_tests.py) | 新增 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
| [tools/verify_package.py](../tools/verify_package.py) | 新增 | 第一方代码/入口 | 源码审查；相关测试/流程验证；平台边界见报告 |
