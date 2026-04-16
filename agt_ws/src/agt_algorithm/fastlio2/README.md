# FAST-LIO2 Preparation

This directory stores project-side preparation files for integrating FAST-LIO2
with the current AGT sensor stack. It is not yet a standalone ROS package.

## Current Sensor Assumptions

- LiDAR driver package: `agt_ws/src/agt_driver/livox_ros_driver2`
- LiDAR launch to use for FAST-LIO2 input: `launch_ROS2/msg_MID360_launch.py`
- LiDAR topic: `/livox/lidar`
- IMU topic: `/livox/imu`
- Current driver frame id: `livox_frame`

## Important Note About Livox Driver Mode

For FAST-LIO2, prefer the Livox driver launch that publishes the customized
Livox message format:

```bash
source install/setup.bash
ros2 launch livox_ros_driver2 msg_MID360_launch.py
```

Do not use `rviz_MID360_launch.py` as the upstream source for FAST-LIO2 setup,
because that launch switches `xfer_format` to `PointCloud2` for visualization.

## Parameter File

Initial parameter template:

- `config/mid360_fastlio2_template.yaml`

Integrated FAST-LIO ROS2 package:

- `FAST_LIO_ROS2/`

Project-specific FAST-LIO MID360 config:

- `FAST_LIO_ROS2/config/agt_mid360.yaml`

Project-specific FAST-LIO launch:

- `FAST_LIO_ROS2/launch/agt_mid360.launch.py`

This template is based on the official FAST-LIO Livox-style configuration and
adapted to the current AGT topic names.

## First-Pass Configuration Strategy

Use the first integration round with:

- `mapping.extrinsic_R = I`
- `mapping.extrinsic_T = 0`
- `mapping.extrinsic_est_en = false`

The goal of this first pass is not final accuracy. It is to verify:

- FAST-LIO2 starts correctly with the current Livox driver topics
- the trajectory is continuous and roughly stable
- there is no obvious frame/sign/topic mismatch

Only after the first trajectory looks reasonable should you spend time on
refined LiDAR-IMU extrinsic calibration.

## Parameters That Still Need Real Calibration

The following values are placeholders and should be calibrated on the real
robot:

- `mapping.extrinsic_T`
- `mapping.extrinsic_R`
- `mapping.acc_cov`
- `mapping.gyr_cov`
- `mapping.b_acc_cov`
- `mapping.b_gyr_cov`

After the first-pass validation, revisit:

- `mapping.extrinsic_T`
- `mapping.extrinsic_R`
- optionally `mapping.extrinsic_est_en`

## Recommended Next Step

1. Keep Livox driver running with `msg_MID360_launch.py`
2. Verify:
   - `/livox/lidar`
   - `/livox/imu`
3. Bring in a FAST-LIO2 package
4. Start from `config/mid360_fastlio2_template.yaml`
5. Calibrate LiDAR-IMU extrinsics before trusting long-run odometry

## Suggested First Run

Start Livox driver in customized message mode:

```bash
source install/setup.bash
ros2 launch livox_ros_driver2 msg_MID360_launch.py
```

Then start FAST-LIO:

```bash
source install/setup.bash
ros2 launch fast_lio agt_mid360.launch.py
```
