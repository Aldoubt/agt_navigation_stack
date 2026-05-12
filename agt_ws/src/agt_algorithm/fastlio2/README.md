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

Integrated PCD-to-Nav2 map package:

- `../agt_pcd2pgm/`

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

## MID360 Warm-Up Note

Before starting mapping, do not begin recording or mapping immediately after
MID360 is powered on.

- Let MID360 run for a while first and wait until the device temperature rises
  to a more stable state
- Starting FAST-LIO mapping too early after a cold start can cause very
  obvious drift
- If the same parameter set sometimes works well and sometimes drifts badly,
  first check whether mapping started before the LiDAR finished warming up

## Automatic Nav2 Map Generation

This workspace now includes `agt_pcd2pgm`, an AGT-local package adapted from
`kzm784/pcd2pgm`, to convert a saved `.pcd` map into a Nav2-compatible
`.pgm + .yaml`.

Package location:

- `agt_ws/src/agt_algorithm/agt_pcd2pgm`

The FAST-LIO MID360 config at `FAST_LIO_ROS2/config/agt_mid360.yaml` now
supports an additional parameter group:

```yaml
pcd_to_nav2_map:
  enable: true
  output_dir: ""
  save_map_name: ""
```

Behavior:

- `enable: true`: convert the saved `.pcd` automatically after FAST-LIO saves
  the point-cloud map
- `output_dir: ""`: save the generated Nav2 map in the same directory as the
  `.pcd`
- `save_map_name: ""`: reuse the `.pcd` filename stem for `.pgm` and `.yaml`

With the default AGT config, pressing `Ctrl+C` after mapping now produces:

- `fastlio_mid360_map.pcd`
- `fastlio_mid360_map.pgm`
- `fastlio_mid360_map.yaml`

all in the same directory as `map_file_path`.

## Manual Conversion

If you already have a `.pcd` map and want to convert it manually:

```bash
cd /home/yangxuan/agt_navigation_stack/agt_ws
source install/setup.bash
export ROS_LOG_DIR=/tmp/ros_logs
ros2 run agt_pcd2pgm agt_pcd2pgm_node --ros-args \
  -p pcd_path:=/absolute/path/to/map.pcd \
  -p output_dir:=/absolute/path/to/output_dir \
  -p save_map_name:=map
```
