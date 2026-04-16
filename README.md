# agt_navigation_stack

面向 **AgroTech 智能机械协会** 的移动机器人导航开发框架。  
目标是提供一套结构清晰、接口统一、便于复现与协作的标准化工程基础，以提升项目开发效率、调试效率与学习效率。

---

## 项目目标

`agt_navigation_stack` 主要用于构建一套可持续演进的导航系统工程框架，覆盖以下核心能力：

- 机器人模型与坐标系管理
- 传感器驱动接入与数据预处理
- 底盘通信与运动控制桥接
- 里程计、定位、建图与导航集成
- 仿真验证与实车部署
- 参数调试、可视化与实验管理
- 接口规范、开发规范与环境复现

该仓库强调：

- **统一目录结构**
- **统一消息与接口规范**
- **统一 TF / Topic 命名习惯**
- **统一测试与部署流程**
- **可复现、可维护、可扩展**

---

## 当前状态

当前版本已完成以下基础内容的初步接入：

- 第一版机器人 URDF 模型
- 阿克曼底盘 CAN 通信与驱动文件

后续工作将围绕导航链路打通、系统标准化与调试工具完善展开。

---

## 仓库结构

```
AGT_navigation_stack/
├── .github/                  # GitHub 平台相关配置
├── docs/                     # 系统文档
│   ├── 整机架构设计
│   ├── 坐标系定义与 TF 树说明
│   ├── Topic / Service / Action 接口说明
│   ├── 包依赖关系
│   ├── 开发规范
│   ├── 硬件接线说明
│   └── 测试验证流程
├── specs/                    # 接口规范与协议说明
├── scripts/                  # 辅助脚本
├── tools/                    # 开发与调试工具
├── docker/                   # 环境复现相关文件
├── third_party/              # 第三方依赖来源、拉取清单与版本说明
│   ├── agt_navigation.repos
│   ├── patch
│   ├── 封装说明
│   └── 版本锁定说明
├── datasets/                 # 数据资产
│   ├── 小型测试数据
│   ├── 示例地图
│   ├── 参数测试基准数据
│   └── 数据说明
└── agt_ws/
    └── src/
        ├── agt_acm_description/      # 机器人描述层
        ├── agt_algorithm/            # 算法隔离层
        │   ├── fastlio2/
        │   ├── rtabmap/
        │   ├── orb_slam3/
        │   └── ...
        ├── agt_bringup/              # 全系统编排层
        │                             # 实车、建图、定位、导航、仿真、模式切换总 launch
        ├── agt_chassis_base/         # 底盘基础通信层
        │   ├── yhs_can_ctrl/
        │   ├── yhs_can_interfaces/
        │   └── 使用说明文档
        ├── agt_chassis_bridge/       # 控制桥接层
        │                             # 输入: /cmd_vel
        │                             # 输出: /ctrl_cmd
        ├── agt_common/               # 全项目通用基础库
        │                             # 坐标系字符串常量、Topic 名称常量、公共工具函数
        ├── agt_driver/               # 传感器驱动层
        │   ├── livox_ros_driver2/    # 雷达驱动、launch、设备参数、基础说明
        │   └── orbbec_sdk/           # 奥比中光相机驱动层
        ├── agt_location/             # 全局定位层
        │                             # map -> odom
        │                             # 输出: /localization_state
        │   ├── icp_relocalization/
        │   ├── amcl/
        │   ├── rtabmap_localization/
        │   ├── rtk_localization/
        │   ├── qrcode_relocalization/
        │   └── ...
        ├── agt_mapping_bringup/      # 建图启动层
        │                             # 不同建图模式对应的 launch 文件
        ├── agt_mission/              # 任务与状态机层
        ├── agt_msgs/                 # 统一消息接口定义
        │   ├── CtrlCmd.msg
        │   ├── ChassisState.msg
        │   ├── VehicleStatus.msg
        │   └── LocalizationState.msg
        ├── agt_nav2/                 # 导航配置层
        │                             # 输入: /tf、/scan 或 PointCloud2
        │                             # 关键坐标系: map、odom
        │   ├── nav2_params.yaml
        │   ├── planner 参数
        │   ├── controller 参数
        │   ├── costmap 参数
        │   ├── behavior tree XML
        │   └── map_server 配置
        ├── agt_odometry/             # 连续运动估计层
        │                             # odom -> base_link
        │                             # EKF / UKF 等融合与滤波
        ├── agt_sensor_proc/          # 传感器预处理层
        │   ├── 点云滤波
        │   ├── IMU 滤波
        │   └── 多传感器时间同步与数据质量检查
        ├── agt_sim_gazebo/           # Gazebo 仿真环境
        │   ├── worlds/
        │   └── ...
        └── agt_tools_gui/            # 工具与可视化层
                                      # 参数控制台、状态仪表盘、实验记录面板
                                      # Topic 监控、TF 可视化辅助、地图资产管理辅助
```

---

## 分层说明

### 1. 描述层
负责机器人模型、连杆结构、传感器外参、碰撞体与可视化模型的统一管理，为仿真、可视化、导航和控制提供一致的机器人描述基础。

### 2. 驱动层
负责各类硬件设备接入，包括激光雷达、相机、IMU、底盘设备等，并提供基础的设备参数配置与启动方式。

当前约定中，`agt_ws/src/agt_driver/` 是驱动目录容器，用于按设备类型组织独立 ROS 包，而不是单独承担一个统一驱动节点。
例如：

- `agt_ws/src/agt_driver/livox_ros_driver2/`
- `agt_ws/src/agt_driver/orbbec_sdk/`

其中每个驱动子目录都应尽量保持为可被 `colcon` 独立发现、独立构建、独立启动的 ROS 包。

`third_party/` 主要用于保存第三方源码来源信息、版本锁定信息和补丁说明，不再作为 Livox 驱动的主要开发位置。

### 3. 预处理层
负责传感器原始数据的轻量化处理，包括去噪、滤波、时间同步、数据质量检查与格式规范化。

### 4. 运动估计与定位层
负责里程计估计、局部位姿跟踪与全局重定位，形成完整的位姿计算链路。

### 5. 导航与任务层
负责路径规划、轨迹跟踪、行为树、任务调度与状态机逻辑，实现从目标输入到执行输出的闭环流程。

### 6. 编排与工具层
负责系统级 launch 编排、模式切换、参数集中管理、调试 GUI 与实验记录支持。

---

## 设计原则

### 统一接口
系统内部尽量使用统一的 Topic、消息、坐标系命名规范，减少模块之间的耦合成本。

### 模块隔离
驱动、算法、导航、任务、仿真、工具等模块尽可能解耦，便于独立调试与替换。

### 优先可复现
环境配置、第三方依赖、参数基线、测试数据尽量固定，确保实验结果可对比、可追踪、可复现。

### 优先可验证
每个模块应具备最小可运行验证路径，避免系统搭建初期过度耦合，降低调试复杂度。

---

## Livox MID360 说明

### 目录位置
当前 Livox 雷达驱动包位于：

`agt_ws/src/agt_driver/livox_ros_driver2/`

第三方拉取来源记录位于：

`third_party/agt_navigation.repos`

常用文件位置：

- 启动文件：`agt_ws/src/agt_driver/livox_ros_driver2/launch_ROS2/`
- 设备配置：`agt_ws/src/agt_driver/livox_ros_driver2/config/`
- 自定义补充配置：`agt_ws/src/agt_driver/livox_ros_driver2/config/agt_driver_driver_config.yaml`

### 常用启动命令
构建单包：

```bash
colcon build --packages-select livox_ros_driver2
```

启动 MID360 驱动并打开 RViz：

```bash
source install/setup.bash
ros2 launch livox_ros_driver2 rviz_MID360_launch.py
```

### MID360 网络配置约定
当前工程中，Livox MID360 的网络配置主要在：

`agt_ws/src/agt_driver/livox_ros_driver2/config/MID360_config.json`

其中需要重点核对两类 IP：

- `host_net_info.*_ip`
  这组地址应填写接雷达那块电脑网卡的实际 IPv4 地址
- `lidar_configs[].ip`
  这组地址应填写 Livox MID360 设备当前真实 IP

如果驱动日志中出现类似：

`found lidar not defined in the user-defined config, ip: 192.168.1.xxx`

通常表示：

- 主机已经发现设备
- 但 `lidar_configs[].ip` 没有写成设备当前真实 IP
- 驱动因此无法为该设备分配索引，可能出现话题存在但 `Publisher count: 0`

### 建议检查顺序
当出现“有 `/livox/lidar` 话题但没有点云”的情况时，建议按下面顺序排查：

1. 检查驱动日志里打印出的设备真实 IP
2. 核对 `MID360_config.json` 中 `lidar_configs[].ip` 是否与日志一致
3. 核对 `host_net_info.*_ip` 是否与本机有线网卡 IP 一致
4. 重新启动驱动后检查：

```bash
source install/setup.bash
ros2 topic info /livox/lidar -v
ros2 topic hz /livox/lidar
```

正常情况下应看到：

- `Publisher count: 1`
- `/livox/lidar` 有稳定频率输出

### FAST-LIO2 建图与保存流程

当前工程中用于 MID360 建图的 FAST-LIO2 包位于：

`agt_ws/src/agt_algorithm/fastlio2/FAST_LIO_ROS2/`

当前默认启动文件：

- `agt_ws/src/agt_algorithm/fastlio2/FAST_LIO_ROS2/launch/agt_mid360.launch.py`
- 默认加载配置：`agt_ws/src/agt_algorithm/fastlio2/FAST_LIO_ROS2/config/agt_mid360.yaml`

开始前请先确认 `agt_mid360.yaml` 中至少包含以下配置：

- `common.lid_topic: "/livox/lidar"`
- `common.imu_topic: "/livox/imu"`
- `publish.map_en: true`
- `pcd_save.pcd_save_en: true`
- `map_file_path: "/home/yangxuan/agt_navigation_stack/datasets/fastlio_mid360_map.pcd"`

推荐流程如下。

1. 构建工作区：

```bash
cd /home/yangxuan/agt_navigation_stack/agt_ws
colcon build --packages-select livox_ros_driver2 fast_lio
source install/setup.bash
```

2. 启动 MID360 驱动：

```bash
cd /home/yangxuan/agt_navigation_stack/agt_ws
source install/setup.bash
ros2 launch livox_ros_driver2 msg_MID360_launch.py
```

3. 新开一个终端，启动 FAST-LIO2 建图：

```bash
cd /home/yangxuan/agt_navigation_stack/agt_ws
source install/setup.bash
ros2 launch fast_lio agt_mid360.launch.py
```

4. 建图完成后，在 FAST-LIO2 所在终端按 `Ctrl+C` 退出。当前工程已经修改为退出时自动保存地图到 `map_file_path`，不需要再手动调用 `/map_save` 服务。

5. 保存成功后，可在终端看到类似输出：

```bash
SIGINT received, saving map to /home/yangxuan/agt_navigation_stack/datasets/fastlio_mid360_map.pcd...
Map saved to /home/yangxuan/agt_navigation_stack/datasets/fastlio_mid360_map.pcd
```

6. 可选检查：

```bash
ls -lh /home/yangxuan/agt_navigation_stack/datasets/fastlio_mid360_map.pcd
pcl_viewer /home/yangxuan/agt_navigation_stack/datasets/fastlio_mid360_map.pcd
```

如果退出时没有保存成功，优先检查以下几项：

- 是否实际启动了 `agt_mid360.launch.py`，而不是默认读取 `mid360.yaml` 的 `mapping.launch.py`
- `publish.map_en` 是否为 `true`
- `pcd_save.pcd_save_en` 是否为 `true`
- `map_file_path` 所在目录是否可写
- 激光雷达和 IMU 是否已经正常输入，地图点云是否已经累计

---

## 规划阶段

### 第一阶段
**目标**：完成基础框架搭建，打通 2D 导航最小可运行链路。

MID360 驱动 → FAST-LIO2 出里程计/点云 → 生成可用地图 → 让 Nav2 先基于这套位姿工作起来

**主要任务**：
- 完成整体工程目录与分层框架搭建
- 明确标准节点、标准 Topic、标准 TF 关系与接口命名
- 完成传感器初始化
- 完成车辆外参标定
- 完成数据链时间同步
- 完成阿克曼速度控制节点的正确转换
- 先跑通基于 Gazebo 的 2D Nav2 导航框架
- 完成仿真传感器接入与基础验证
- 完成调试测试台 GUI 的初版开发
  - 支持节点快速启动
  - 支持组合测试
  - 支持参数显示与调节
  - 支持参数保存与加载

当前已在仓库中预留 FAST-LIO2 侧参数准备目录：

- `agt_ws/src/agt_algorithm/fastlio2/README.md`
- `agt_ws/src/agt_algorithm/fastlio2/config/mid360_fastlio2_template.yaml`

### 第二阶段
**目标**：完成建图、重定位与导航链路增强，并逐步形成更稳定的实用方案。

**主要任务**：
- 在 RViz 中正确显示高精度 URDF 模型与简化模型
- 前端先使用 Fast-LIO2 估计局部位姿
- 初期不融合轮速传感器
- 使用 ICP 实现重定位
- 实现建图与导航流程联调
- 建立切换式导航模式
- 基于二维码识别与先验地图实现稳定路径规划与导航
- 深入理解 Cartographer 原理
- 在理解算法原理基础上补充前处理模块
- 建立实验评价指标
- 开展参数优化与实验验证

### 第三阶段
**目标**：在现有导航系统基础上引入轻量化感知增强与语义信息，为后续创新功能提供支撑。

**主要任务**：
- 在传感器数据进入系统前进行轻量化预处理
- 为环境数据增加语义信息
- 基于语义信息提升系统能力与研究创新空间
- 尝试倾斜安装 MID360
- 利用顶棚与地面结构信息优化重定位效果

---

## 建议优先补充的文档

为保证后续开发效率，建议优先在 `docs/` 中补齐以下内容：

- 系统总体架构图
- TF 树定义
- Topic / Service / Action 接口表
- 坐标系命名规范
- 底盘控制接口说明
- 传感器外参与标定流程
- 建图 / 定位 / 导航启动说明
- 仿真测试流程
- 参数管理规范
- 提交与分支协作规范

---

## 后续方向

该仓库后续可进一步扩展为：

- 面向协会内部成员的标准开发模板
- 面向不同底盘与传感器组合的导航基线工程
- 面向比赛与科研项目的复用型基础框架
- 面向实车部署、仿真验证与实验记录的一体化平台

