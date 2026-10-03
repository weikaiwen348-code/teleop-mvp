# 机器人遥操作框架：Panda 仿真与示教采集

v0.2 可运行交付：浏览器滑块 → 七关节同构映射 → 软件控制状态机 → Franka Panda 公共 MuJoCo 模型 → 轨迹记录与 NPZ 导出。另有双进程 UDP 通信与延迟、丢包、断流实验。

本次完成软件框架和仿真验证。未接入实体 GELLO、Franka/UR，也未测量跨地域网络、物理精度或双向力反馈。`panda` 使用公开模型中的关节、惯性、重力、碰撞几何和夹爪；它不是经过实机参数标定的数字孪生。

## 全组从这里开始（2026-10-03 团队说明更新）

第一次接触本项目，请先读 **[全组新手指南](docs/TEAM_GUIDE.md)**，按步骤运行一次再准备答辩。

- [v0.1 与 v0.2 的具体区别](docs/VERSION_COMPARISON.md)
- [所有材料的完整索引](docs/MATERIAL_INDEX.md)
- [组员任务、验收与后续路线](docs/TEAM_TASKS.md)
- [GitHub 更新状态与协作方法](docs/GITHUB_UPDATE.md)

本次只补充和修订文档，运行软件仍为 v0.2.0。GitHub 目标仓库当前返回 404，尚未完成远端更新；需先确认仓库链接和连接授权。

## 直接演示

解压后，在本目录打开终端，使用 Python 3.10+：

```bash
python -m pip install -e '.[demo]'
python -m teleop ui --output runs/manual-01 --open-browser
```

浏览器地址默认为 `http://127.0.0.1:8080`，需要支持 WebGL 的现代浏览器。模型、网格和浏览器脚本均随工程提供，运行时无需联网下载。首次安装 Python 依赖需要联网。

1. 等待 Panda 加载，点击“开启跟随”。程序会先对齐当前关节位置。
2. 小幅拖动关节滑块，观察机械臂跟随；夹爪滑块的 0% 表示打开，100% 表示闭合。
3. 点击“暂停指令发送”，观察超时进入 HOLD。恢复发送后仍需点击“开启跟随”。
4. 点击“软件急停”，观察锁定；点击“本地复位”后重新使能。
5. 点击“结束并保存”，看到保存完成后，在终端按 Ctrl+C 退出。

每次使用新的输出目录，避免覆盖已有示教。完成目录包含 `steps.jsonl`、`metadata.json`、`summary.json` 和 `episode.npz`。检查方式：

```bash
python -m teleop inspect runs/manual-01
python -m unittest discover -s tests -v
```

界面绘图与指令心跳分开：Web Worker 约每 30 ms 请求机器人端有效期并发送当前滑块目标；Python 控制线程以目标 100 Hz 运转。实际频率取决于电脑负载。退出浏览器或关闭心跳会导致机器人端保持。软件 HOLD 使用仿真数值冻结，不能替代实体机器人减速、制动或硬件急停。

## 仿真与远程链路

```bash
# 公开 Panda 模型，自动采用七关节 Panda 配置
python -m teleop sim --output runs/panda --backend panda --duration 6
# 按墙钟时间播放
python -m teleop sim --output runs/panda-live --backend panda --realtime --duration 6
# 一阶模型，用于快速复现通信故障
python -m teleop sim --output runs/blackout --blackout-at 3 --duration 6
```

`toy` 是一阶模型；`mujoco` 是旧版通用关节链，关闭重力和碰撞；`panda` 是本次新增的公开 Panda 模型。旧 `panda7_sim.json` / `ur6_sim.json` 是示例关节配置；`configs/panda_model.json` 与本次 Panda 模型匹配。六关节 UR 模式只有通用仿真，没有 UR 实体模型或驱动。

双进程 UDP 示例：

```bash
python -m teleop keygen demo.key
# 终端 A：Panda 仿真服务器
python -m teleop server --backend panda --config configs/panda_model.json --keyfile demo.key --output runs/server --duration 30
# 终端 B：虚拟 GELLO 输入
python -m teleop client --config configs/panda_model.json --keyfile demo.key --virtual --duration 20
```

`--virtual` 自动生成关节轨迹。GELLO 可选输入封装保留在 `network.py`，串口硬件尚未测试。不加 `--virtual` 时使用终端 `a/h/e/q` 开关；未指定 `--gello-config` 时仍使用合成关节轨迹，不是实物手柄输入。

两台电脑需使用相同配置和共享密钥，并明确指定 `--host`。UDP HMAC 校验完整性，不加密；远程使用受控 VPN。默认只监听本机。浏览器 UI 是本地演示入口，不是已部署的远程 Web 服务。密钥不要加入版本库。

## 映射与数据语义

同拓扑、同关节顺序时：

`q_target = reference + signs * gains * (q_leader - offsets)`

可用多姿态最小二乘拟合符号、比例和零位：

```bash
python -m teleop calibrate examples/calibration_pairs.json runs/calibration.json
```

该示例是合成标定数据。7 关节 Panda 与 6 关节 UR 不能直接逐关节互映；本版会拒绝维度不一致，未实现异构 IK 重定向。

每行先记录执行前 `observation.q/dq/gripper`，再记录随后下发的 `action.q/gripper`，另存未经限速的映射目标 `target.q`。NPZ 保留全部时间戳，并用 `valid` 标记 ACTIVE 行。任务成功 `success=null`，不能把一段正常保存的轨迹自动标成成功任务。当前导出是本项目 schema，不是已转换好的 LeRobot/RLDS 数据集；没有相机、触觉或力矩数据。

## 工程与答辩材料

- `teleop/panda.py`：公共 Panda 模型接口；`teleop/manual.py`、`teleop/web/`：本地交互界面。
- `teleop/mapping.py`、`control.py`、`protocol.py`：映射、约束和状态机、有效期与报文检查。
- `teleop/network.py`、`simulation.py`、`recording.py`：通信、扰动实验、完整性检查与导出。
- `tests/`：29 项通过的测试；`reports/RESULTS_V02.md`：本次验证；`reports/RESULTS.md`：旧版实验。
- `manual_demo_episode/`：通过自动操作真实浏览器界面产生的 Panda 仿真示例，非实体 GELLO 或人类任务数据。
- `defense/`：结题 PPT、演示视频、讲稿问答、操作卡和逐页预览。

答辩建议标题：“机器人遥操作框架设计与仿真验证”。请按实际完成范围陈述；原项目中的硬件集成和跨地域实验尚未完成。GELLO 与 Franka/UR 的适配已有先例，本项目的贡献是软件复现、状态约束和数据流整合，不宣称首次适配或新型重定向算法。

开源来源与许可证见 `docs/SOURCES.md`、各资源的 `SOURCE.json` 和 LICENSE。可继续实机工作的接口与步骤见 `docs/HARDWARE.md`。
