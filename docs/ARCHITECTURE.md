# Architecture Design (架构设计)

## System Overview (系统概览)

AGT Navigation Stack is designed with a layered architecture to provide modularity, maintainability, and extensibility.

## Layered Architecture (分层架构)

### 1. Hardware Abstraction Layer (硬件抽象层)
- **Components**: `agt_driver`, `agt_chassis_base`
- **Responsibility**: Raw hardware communication
- **Output**: Raw sensor data, hardware state
- **Update Rate**: 100 Hz (IMU), 20 Hz (Chassis), 10 Hz (Lidar/Camera)

### 2. Sensor Processing Layer (传感器处理层)
- **Components**: `agt_sensor_proc`
- **Responsibility**: Filtering, preprocessing, temporal alignment
- **Processing**:
  - Lidar: Voxel downsampling, outlier removal
  - IMU: Zero-drift compensation, temperature drift correction
  - Camera: Distortion correction, feature detection
- **Output**: Filtered, synchronized sensor data
- **Latency**: <50ms

### 3. Estimation Layer (估计层)
- **Components**: `agt_odometry`
- **Responsibility**: Motion estimation and pose tracking
- **Methods**:
  - EKF: Extended Kalman Filter
  - UKF: Unscented Kalman Filter
  - Fusion: Sensor fusion of Lidar, IMU, Wheel encoders
- **Output**: Local odometry (odom → base_link)
- **Frequency**: 20 Hz

### 4. Localization Layer (定位层)
- **Components**: `agt_location`
- **Methods Available**:
  - AMCL: Adaptive Monte Carlo Localization
  - ICP: Iterative Closest Point
  - RTK: Real-Time Kinematic GPS
  - RTAB-Map: Real-Time Appearance-Based Mapping
  - QR Code: Prior map-based QR code relocation
- **Output**: Global pose (map → odom)
- **Frequency**: 10 Hz

### 5. Mapping & SLAM Layer (建图层)
- **Components**: `agt_mapping_bringup`
- **Algorithms**:
  - Slam Toolbox: Graph-based SLAM
  - Cartographer: Real-time SLAM
- **Output**: Occupancy grid map
- **Format**: PNG image + YAML metadata

### 6. Navigation Layer (导航层)
- **Components**: `agt_nav2`
- **Features**:
  - Global planner (Navfn, Smac)
  - Local controller (DWB, Regulated Pure Pursuit)
  - Costmap management
  - Behavior trees
- **Input**: Goal pose, map, sensor data
- **Output**: Velocity commands
- **Frequency**: 20 Hz

### 7. Mission & Planning Layer (任务层)
- **Components**: `agt_mission`
- **Responsibility**: High-level mission planning
- **Features**:
  - Goal sequencing
  - State machine management
  - Error recovery
  - Mission logging

### 8. Tools & Visualization Layer (工具层)
- **Components**: `agt_tools_gui`, `agt_bringup`
- **Features**:
  - Parameter management
  - Runtime debugging
  - RViz visualization
  - System monitoring

## Data Flow (数据流)

```
Hardware Sensors
       ↓
[agt_driver] - Raw sensor data
       ↓
[agt_sensor_proc] - Filtered data
       ↓
      ├→ [agt_odometry] → /odom topic
      │
      ├→ [agt_location] → /localization_state, /tf (map→odom)
      │
      └→ [agt_mapping_bringup] → /map, map file
            ↓
         (saved map used for localization)
       ↓
[agt_nav2] + [agt_mission] - Planning & Navigation
       ↓
[agt_chassis_bridge] - Command translation
       ↓
[agt_chassis_base] - Hardware control
       ↓
Physical Hardware (Motors, etc.)
```

## Design Patterns (设计模式)

### 1. Node-based Modularity
- Each functional block is a separate ROS 2 node
- Nodes communicate via topics/services
- Easy to enable/disable components

### 2. Configuration Management
- YAML-based configuration
- Per-package config files
- Runtime parameter adjustment

### 3. Error Handling
- Timeout management (5-10 seconds typically)
- Watchdog timers for critical nodes
- Graceful degradation

## Dependencies (依赖关系)

```
agt_bringup (orchestrator)
    ├── agt_acm_description (URDF)
    ├── agt_chassis_bridge
    │   ├── agt_msgs
    │   ├── agt_common
    │   └── geometry_msgs
    ├── agt_odometry
    │   ├── agt_msgs
    │   ├── agt_common
    │   ├── nav_msgs
    │   └── tf2_ros
    ├── agt_location
    │   ├── nav2_*
    │   └── ...
    └── agt_nav2
        ├── nav2_bringup
        ├── nav2_planner
        └── nav2_controller
```

## Extension Points (扩展点)

1. **New Localization Method**: Add new node in `agt_location`
2. **Custom Algorithm**: Add to `agt_algorithm` layer
3. **New Sensor Type**: Add to `agt_driver` and `agt_sensor_proc`
4. **GUI Enhancement**: Extend `agt_tools_gui`
5. **Mission Logic**: Add state machine to `agt_mission`

## Performance Targets (性能目标)

- **Localization Accuracy**: ±5cm (indoors), ±1m (outdoors with RTK)
- **Navigation Speed**: 0.1-1.5 m/s
- **System Latency**: <200ms (sensor to action)
- **Uptime**: >99% during normal operation
- **CPU Usage**: <80% on single core
- **Memory**: <500MB basic, <1.5GB with SLAM active

## Quality Attributes (质量属性)

### Reliability
- Redundant sensors where critical
- Graceful fallback mechanisms
- Regular health checks

### Maintainability
- Clear separation of concerns
- Well-documented code
- Consistent naming conventions

### Extensibility
- Plugin-based approach for algorithms
- Configuration-driven behavior
- Loose coupling between modules

### Performance
- Optimized message sizes
- Efficient algorithms
- Resource-aware processing
