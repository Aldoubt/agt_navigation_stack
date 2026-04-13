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

| Frame | Description | Parent | Type |
|-------|-------------|--------|------|
| map | Global fixed reference frame | - | Fixed |
| odom | Odometry reference frame | map | Dynamic (TF broadcast) |
| base_link | Robot main body | odom | Dynamic (TF broadcast) |
| lidar_link | LiDAR sensor | base_link | Fixed (TF broadcast) |
| camera_link | Camera sensor | base_link | Fixed (TF broadcast) |
| imu_link | IMU sensor | base_link | Fixed (TF broadcast) |

## Transformation (变换关系)

### map -> odom
- Published by: `agt_location` (localization node)
- Frequency: 10 Hz
- Represents: Global localization offset

### odom -> base_link
- Published by: `agt_odometry` (odometry node)
- Frequency: 20 Hz
- Represents: Robot pose relative to odometry frame

### base_link -> sensors
- Published by: Static TF broadcasters at startup
- Type: Fixed transforms
- Contains: Sensor mounting offsets

## Usage in Code

```python
import tf2_ros
from geometry_msgs.msg import TransformStamped

# Lookup transform
tf_buffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tf_buffer)

# Get transform from map to base_link
try:
    transform = tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
except tf2_ros.TransformException:
    # Handle exception
    pass
```

## Parameters (参数设置)

- **TF Lookup Timeout**: 5.0 seconds
- **Update Frequency**: 20-100 Hz (topic dependent)
- **Position Precision**: 0.001 m
