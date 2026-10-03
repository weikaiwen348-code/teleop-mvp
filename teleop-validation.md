# v0.2 仿真与交互验证报告

验证日期：2026-10-03。完成范围：公开 Panda 模型集成、本地七关节交互、输入超时与软件急停、轨迹完整保存。实体 GELLO、Franka/UR、力反馈、跨地域和相机同步均未验证。

## 模型与运行环境

- Python 3.12.14、NumPy 2.3.5、MuJoCo 3.3.7；Linux。
- MuJoCo Menagerie `franka_emika_panda`，commit `4d038b3feae26ec82b46a4d586379114012a8ac7`；上游 XML 未修改，保留许可证、关节结构、惯性、重力、碰撞几何和原生夹爪执行器。
- 模型 9 个速度自由度（7 个机械臂关节、2 个手指关节），8 个执行器。保留碰撞几何不等于实现主动避碰或实机碰撞验证。
- 本地 Three.js 0.180.0 绘制 MuJoCo 编译网格与实时姿态；Web Worker 心跳约每 30 ms 运行。Python 控制目标 100 Hz，物理固定步长 10 ms，看门狗使用墙钟单调时间。

## 测试与交互证据

29 项单元/集成测试通过，完整输出 `tests-v02.txt`。新增测试检查原生模型/夹爪跟随、配置超出模型范围拒绝、本地急停复位与重新使能、非法角度与旧会话拒绝、完整导出，以及固定目标收敛、无参考轨迹极限环，以及虚拟输入等待慢启动后端后从零位开始。

实际浏览器按钮和滑块检查通过：关节跟随、夹爪闭合、发送暂停后 HOLD、重新使能、急停与复位、结束完整导出、缺失本地 token 的写请求拒绝；页面脚本错误为 0。记录方式是自动鼠标/按钮操作真实运行界面。视频不是实体实验或人类操作研究，样例元数据 `human_collected=false`。

独立构建 wheel 后，模型和 Web Worker 资源存在，并能从解压安装包加载模型（8 执行器、59 个 OBJ 网格资源）。测试没有要求运行时联网获取模型。

## 本次界面演示实测

| 指标 | 值 | 含义 |
|---|---:|---|
| 总采样行数 | 3517 | 含所有状态 |
| ACTIVE / valid 行数 | 2302 | 标记为有效执行区间 |
| 墙钟运行时间 | 35.43 s | 单次本机演示 |
| 平均控制频率 | 99.26 Hz | Python 仿真线程 |
| 周期间隔 P95 | 11.76 ms | 含系统调度抖动 |
| 接受 / 拒绝指令 | 573 / 0 | HTTP 操作端正常链路 |
| 最后接受指令至 HOLD | 115.86 ms | 非实体制动时间 |
| 全关节观测相对上一拍动作 RMSE | 0.005247 rad | 仅相邻两行都为 ACTIVE |
| 第 1 关节同口径 RMSE | 0.008585 rad | 小幅仿真演示，非算法对照 |

频率不是网络单向延迟；数据也不包括视频回传或物理机器人。RMSE 来自仿真状态，无末端外部测量，不能声称毫米级精度。没有长期稳定性测试。

## 状态事件

| 仿真服务器相对墙钟 / s | 状态 | 原因 |
|---|---|---|
| 0.000 | DISARMED | startup |
| 3.964 | ACTIVE | armed |
| 22.094 | HOLD | input_timeout |
| 25.866 | ACTIVE | armed |
| 30.863 | ESTOP | local_ui_estop |
| 33.721 | DISARMED | local_reset |

HOLD 和 ESTOP 为仿真数值冻结。120 ms 机器人端有效期先于 150 ms 接收看门狗到期；更新 epoch 后不能用旧使能自动恢复。

## 数据完整性

`manual_demo_episode` 的 metadata.complete 为真，行数与时间戳单调性、SHA-256 检查通过，NPZ 数组形状为 ({m['rows']}, 7)。JSONL 记录执行前 observation 与随后 action，另存 target。NPZ 保留所有行及 valid 掩码。success=null；没有语义成功自动标注、相机、力传感器或训练结果。

PPT 第六页选取首次 ACTIVE 后七秒的第 1 关节片段，每约 12 行抽样；时间保留三位小数，图表角度值保留六位小数以便 Excel 编辑，原始日志不变。

## 复现

```bash
python -m pip install -e '.[demo]'
python -m unittest discover -s tests -v
python -m teleop ui --output runs/new-manual --open-browser
python -m teleop sim --backend panda --output runs/new-panda --duration 2
python -m examples.loopback_validation --backend panda --output runs/new-panda-udp
```

旧版 23 项测试、通用模型和网络场景报告保存在 `RESULTS.md`、`validation.json`、`loopback.json`，不要把旧通用模型结果混为此次 Panda 物理模型测试。

## 未完成项

实体手柄/机械臂通信、实机动力学对齐、厂家实时伺服、实体急停与使能、停止距离与物理误差、远程部署、双向力反馈、相机与状态同步、异构 IK、LeRobot/RLDS 转换、语义自动标注及模仿学习训练均未完成。

## Panda 双进程本机 UDP 验证

使用相同 Panda 配置，操作端为合成输入，机器人端为公开 Panda 模型。独立检查通过：接受 250 条、拒绝 0 条，客户端退出后进入 HOLD/input_timeout，日志记录了超时事件。服务器墙钟 5.02 s，平均频率 98.89 Hz，周期 P95 10.06 ms。指令发送至确认的 P95 为 10.33 ms，最后接受指令至 HOLD 为 119.99 ms。确认时间包含服务器调度，不是单向网络延迟，不包含实体机械臂或视频。原始文件 `panda-loopback.json`，检查标记 passed=true。

复测中发现两个问题：虚拟客户端在后端慢启动期间提前推进合成轨迹，会超出使能对齐容差；现已将合成轨迹起点移到首次收到后端状态之后，并增加延迟启动集成测试。在与视频编码和 PPT 渲染同时运行的一次检查中，服务器出现 control_deadline FAULT，说明 Python 进程无法保证受负载影响时的硬实时；该事件通过本地状态机冻结仿真。保留的失败日志为 `panda-loopback-load-fault.json`；独立检查不并行运行重负载作业后通过。这个观察不构成长时间压力测试或可承诺的性能边界。

固定目标参考轨迹曾出现过冲，现加入目标位置制动约束并通过收敛测试；本报告和 PPT 的演示数据均在修正后重新录制。
