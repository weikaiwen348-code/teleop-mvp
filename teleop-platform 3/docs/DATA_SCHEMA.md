# 示教数据协议 v1.0

每次运行产生独立目录：`metadata.json`、`steps.jsonl`、`summary.json`。每行是一次机器人端控制步骤；所有角度为 rad，关节速度为 rad/s，时间为 s。

| 字段 | 含义 |
|---|---|
| step / t_robot_s | 连续行号；同一机器人的单调递增相对时间 |
| observation.q / dq | 本次动作下发前的实测/模拟关节状态 |
| observation.gripper | 执行前夹爪状态，0 开 1 闭；toy/通用链为模拟标量，panda 来自模拟手指关节 |
| action.q / action.gripper | 本次准备执行的受限绝对目标 |
| target.q | 最新经接受的原始关节目标，用于分析限速影响 |
| source_seq | 最新被控制状态机消费的序号；HOLD/未使能时不代表有效训练动作 |
| rx_robot_s | 最新 ACTIVE 目标接受的机器人本地时间，无则 null |
| source_sim_s | 仅模拟场景中的源采样时间；真实双进程为 null |
| mode / event | 控制状态与最近状态事件原因 |
| sample_weight | ACTIVE=1，其余=0；只是候选训练掩码，不是成功标签 |

元数据包含完整配置与配置哈希、软件场景、时间域、后端类型、单位、动作语义和 writer 状态。`success=null`、`success_source=unlabeled` 是明确的未知标签，不能自动改成成功。

自动生成的是结构化字段（时间、关节状态、动作、模式和质量标记）。抓取是否成功、插入是否到位等语义标签仍需人工审核或经验证的任务传感器。仅凭程序正常退出不能判定任务成功。

NPZ 内：`observation[T,N]`、`action[T,N]`、`target[T,N]`、`gripper_observation[T]`、`gripper_action[T]`、`timestamp[T]`、`valid[T]`、`metadata_json`。无需 `allow_pickle=True`。不隐式重采样，不把 HOLD 前后拼成无缝序列。

后续视觉/力数据需增加：相机标识、frame index、曝光中点时间、时钟域、与关节状态对齐的时间误差、标定版本、末端位姿坐标系、力/力矩单位和坐标系。视频宜独立编码存储；控制环不能等待编码或写盘。受控主机内优先使用同一单调时钟；跨设备需要验证的同步或时钟变换及误差上界。

尚未实现：摄像头采集、视频回传、力传感器、自动任务阶段切分、LeRobot/RLDS 转换、数据集切分和训练。真实示教数据应按完整 episode 划分训练/验证，避免邻近帧泄露到两侧。

## v0.3 检查与来源补充

新记录增加 `software_version`；网页来源标记 `human_collected=null`，不自动声称人工示教。已有 v0.2 文件未补写软件版本或改写原始数据。

读取时重新验证配置内容与配置哈希、完整标志、写盘错误、行数、逐行字段、有限时间/数值、模式与 sample_weight 一致性。NPZ 导出拒绝覆盖已有文件，失败清理本次新建的半成品。`quality` 检查进一步逐项比较 JSONL 与 NPZ 数组、valid 的布尔类型、内嵌元数据和运行摘要。SHA-256 用于发现内容变化，不提供对恶意重算哈希的数字签名保证。

`metadata.complete` 表示原始 JSONL 完整关闭；网页 `summary.complete` 表示本次关闭和 NPZ 导出也成功。任务 `success` 仍单独为未知。v0.3 报告的平均采样频率为 `(N-1)/(t_last-t_first)`，与旧摘要的 `N/elapsed_wall_s` 不同。跟踪 RMSE 配对当前观测与上一拍执行动作，且只使用相邻两行都为 ACTIVE 的样本；它不代表末端绝对精度。
