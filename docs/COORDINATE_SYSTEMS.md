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
- 发布节点：`agt_location`（定位节点）
- 发布频率：10 Hz
- 含义：表示全局定位偏移量

### odom -> base_link
- 发布节点：`agt_odometry`（里程计节点）
- 发布频率：20 Hz
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

- **TF 查询超时**：5.0 秒
- **更新频率**：20-100 Hz（取决于具体 topic）
- **位置精度**：0.001 m
