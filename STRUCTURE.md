# AGT Navigation Stack Project Structure

## 目录结构说明

```
AGT_navigation_stack/
├── .github/              # GitHub平台相关配置
├── docs/                 # 系统文档
├── specs/                # 接口规范
├── scripts/              # 辅助脚本
├── tools/                # 开发与调试工具
├── docker/               # 容器化环境
├── third_party/          # 第三方依赖
├── datasets/             # 数据资产
└── agt_ws/               # ROS2工作区
    └── src/
        ├── agt_msgs/     # 消息定义
        ├── agt_common/   # 通用工具库
        ├── agt_acm_description/    # 机器人描述
        ├── agt_chassis_base/       # 底盘通信
        ├── agt_chassis_bridge/     # 控制桥接
        ├── agt_driver/             # 传感器驱动
        ├── agt_sensor_proc/        # 传感器预处理
        ├── agt_algorithm/          # 算法隔离
        ├── agt_odometry/           # 里程计估计
        ├── agt_location/           # 全局定位
        ├── agt_mapping_bringup/    # 建图启动
        ├── agt_nav2/               # 导航配置
        ├── agt_mission/            # 任务规划
        ├── agt_tools_gui/          # 可视化工具
        ├── agt_sim_gazebo/         # 仿真环境
        └── agt_bringup/            # 总启动文件
```

## 快速开始

### 1. 环境配置

#### Docker方式（推荐）
```bash
cd docker
docker-compose build
docker-compose run agt_nav
```

#### 本地编译
```bash
cd agt_ws
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

### 2. 启动系统
```bash
ros2 launch agt_bringup agt_bringup.launch.xml
```

### 3. 主要功能模块

- **底盘控制**: `agt_chassis_bridge` - 将 `/cmd_vel` 转换为 `/ctrl_cmd`
- **里程计**: `agt_odometry` - 发布 `/odom` 话题
- **定位**: `agt_location` - 提供全局定位 `/localization_state`
- **导航**: `agt_nav2` - Navigation2 栈配置
- **建图**: `agt_mapping_bringup` - SLAM和建图启动

## 文件说明

### 消息定义 (agt_msgs/)
- `CtrlCmd.msg` - 控制命令
- `ChassisState.msg` - 底盘状态
- `VehicleStatus.msg` - 车辆状态
- `LocalizationState.msg` - 定位状态

### 配置文件 (requirements/配置)
- `agt_navigation.repos` - 依赖清单
- `requirements.txt` - Python依赖
- `docker/Dockerfile` - Docker构建配置
- `docker/docker-compose.yml` - Docker编排配置

## 开发规范

详见 `docs/` 目录

## 许可证

Apache 2.0 License
