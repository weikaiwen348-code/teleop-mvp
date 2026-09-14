# teleop-mvp
同济大学机器人遥操作平台sitp
# Teleoperation MVP

## 第一阶段目标

在仿真中完成真机测试所需的统一机器人接口、安全控制、测试脚本和日志系统，并通过真机准入检查。

## 第一次真机测试范围（可用真机型号：ur5，Franka3）

1. 连接机器人
2. 读取关节状态
3. 保持当前位置
4. 受限单关节运动
5. 停止与超时保护
6. 保存运行日志

## 暂时不做

- 完整GELLO遥操作
- ROS 2系统重构
- Gazebo
- 视觉
- 模仿学习
- 跨地域网络

## 接口确定
class Robot:
    def is_connected(self) -> bool:
        ...

    def get_joint_state(self):
        ...

    def command_joint_position(self, q_target):
        ...

    def stop(self):
        ...
现在不要求实现，但全组必须接受：

上层控制程序只能调用这个接口，不能到处直接调用MuJoCo或真机驱动。

以后对应关系是：

SimRobot  → MuJoCo
RealRobot → 真实机械臂驱动

这样仿真验证后的Safety、Logger和测试脚本才能复用于真机。