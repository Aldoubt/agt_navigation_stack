# Coordinate System Definition (坐标系定义)

## Frame Hierarchy (坐标系层次结构)

```
map
 └── odom
      └── base_link
           ├── lidar_link
           ├── camera_link
           └── imu_link
```

## Frame Descriptions (坐标系描述)

| Frame | 描述 | 父坐标系 | 类型 |
|-------|------|----------|------|
| map | 全局固定参考坐标系 | - | 固定 |
| odom | 里程计参考坐标系 | map | 动态（通过 TF 广播） |
| base_link | 机器人主体坐标系 | odom | 动态（通过 TF 广播） |
| lidar_link | LiDAR 传感器坐标系 | base_link | 固定（通过 TF 广播） |
| camera_link | 相机传感器坐标系 | base_link | 固定（通过 TF 广播） |
| imu_link | IMU 传感器坐标系 | base_link | 固定（通过 TF 广播） |

## Transformation (变换关系)

### map -> odom
- 当前状态：在现有 bringup / odometry launch 中由 `static_transform_publisher` 发布为静态零变换
- 推荐配置：当启用 `agt_location` 且基于 MID360 点云做定位时，可按 5-10 Hz 动态发布，10 Hz 可与 MID360 典型点云帧率对齐
- 含义：表示全局定位偏移量

### odom -> base_link
- 目标发布节点：`agt_odometry`（里程计节点）
- 推荐发布频率：不低于 30 Hz；对 30 Hz 阿克曼底盘应至少与底盘反馈/控制周期一致，最好由底盘反馈触发
- 含义：表示机器人相对于 `odom` 坐标系的位姿

### base_link -> sensors
- 发布方式：启动时由静态 TF 广播器发布
- 类型：固定变换
- 内容：传感器安装位姿偏移

## Usage in Code (代码中的使用示例)

```python
import tf2_ros
from geometry_msgs.msg import TransformStamped

# 查询变换
tf_buffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tf_buffer)

# 获取从 map 到 base_link 的变换
try:
    transform = tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
except tf2_ros.TransformException:
    # 异常处理
    pass
```

## Parameters (参数设置)

- **TF 查询超时**：建议 0.1-0.2 秒；不建议写成 5.0 秒这类过大的运行时容忍值
- **`odom -> base_link` 更新频率**：建议 >= 30 Hz，并与阿克曼底盘反馈周期保持一致
- **`map -> odom` 更新频率**：静态场景为 0 Hz；若由 MID360 点云定位驱动，建议 5-10 Hz，10 Hz 为常见配置
- **数值表示分辨率**：0.001 m 可作为坐标数值分辨率，但不能视为整车实际定位精度
