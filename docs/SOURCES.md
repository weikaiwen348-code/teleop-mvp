# 来源与立项修正

核查日期：2026-09-29。下列是论文作者、项目维护者或厂家的第一手来源；链接会更新，硬件接入时应固定实际使用版本。

1. Wu 等，GELLO 原论文（2023）：https://arxiv.org/abs/2309.13037 。原文说明已设计 Franka、UR5、xArm 系统，因此“首次适配 Franka/UR”不是本项目成立的创新点。
2. GELLO 官方软件仓库：https://github.com/wuphilipp/gello_software 。本次读取 README 与 `gello/agents/gello_agent.py`；已有 Panda/UR 后端与关节 offset/sign 配置。未把完整上游代码复制进本工程，也未在硬件上验证其兼容性。
3. Franka FCI：https://frankarobotics.github.io/docs/ 。区分 FR3 与 FER/Panda，并检查系统和库兼容性。
4. Franka 最低系统与网络要求：https://frankarobotics.github.io/docs/doc/libfranka/docs/system_requirements.html 。Linux PREEMPT_RT、本地低延迟网络与控制周期要求支持本工程“远程目标、本地伺服”的设计判断。
5. UR 官方 RTDE 指南：https://docs.universal-robots.com/tutorials/communication-protocol-tutorials/rtde-guide.html 。e-Series/ur-Series 可输出至控制周期频率，但控制器资源不足时可跳包；协议输出频率不等同于已实现运动闭环。
6. MuJoCo Python 文档：https://mujoco.readthedocs.io/en/stable/python.html 。Python binding 与 macOS `mjpython` 被动查看器使用说明。本工程依赖固定在 3.3.7，文档 stable 页面可能高于此版本；核心 API 已在 3.3.7 实测。
7. Sujit 等（2025），Improving Low-Cost Teleoperation: Augmenting GELLO with Force：https://arxiv.org/abs/2507.13602 。已存在对 GELLO 增加力信息与反馈的研究；不能把普通位置映射写成已实现高精度力反馈。

工程判断：优先完成硬件标定、本地安全控制、故障行为和数据同步，是可实施的项目范围收敛。关于论文可发表性、相对性能提升和跨地域效果，本文没有实验证据，不作既成结论。

## v0.2 新增资源（2026-10-03）

- Franka Panda 模型：Google DeepMind MuJoCo Menagerie，https://github.com/google-deepmind/mujoco_menagerie/tree/4d038b3feae26ec82b46a4d586379114012a8ac7/franka_emika_panda 。保留该目录的 Apache-2.0 LICENSE；上游 panda.xml 与 scene.xml 未修改。Python 关节适配和网页显示为本工程新增。
- Three.js：官方 npm `three@0.180.0`，https://www.npmjs.com/package/three/v/0.180.0 。保留 MIT 许可证 `teleop/web/THREE_LICENSE.txt`。本地包含 three.module.js、three.core.js、OrbitControls.js。
- PPT 和演示图使用本次真实运行的仿真界面截图，不代表实体机器人照片。示例视频由脚本操作浏览器滑块和按钮录制，不是人类操作研究或实机实验。
