# README for AGT Bringup Package

## Overview

The `agt_bringup` package is the main orchestration layer for the AGT Navigation Stack. It provides launch files and configurations for starting the complete system.

## Launch Files

### agt_bringup.launch.xml
Main launch file that starts all essential components:
- Robot description (URDF + TF)
- Chassis bridge
- Odometry estimation
- Static transforms (map → odom)

Usage:
```bash
ros2 launch agt_bringup agt_bringup.launch.xml
```

## Configuration Files

### agt_robot_params.yaml
Main parameter file containing:
- Robot physical specifications
- Velocity and acceleration limits
- Sensor configurations
- Filter type and parameters
- Localization method
- Navigation tolerances

## Launch Modes

### Basic Mode (No Localization)
```bash
ros2 launch agt_bringup agt_bringup.launch.xml use_localization:=false
```

### With AMCL Localization
```bash
ros2 launch agt_bringup agt_bringup.launch.xml localization_method:=amcl
```

### Simulation Mode
```bash
ros2 launch agt_bringup agt_bringup.launch.xml use_sim_time:=true
```

## Important Services

- `start_mapping`: Begin SLAM mapping
- `stop_mapping`: End SLAM mapping
- `save_map`: Save current map to disk

## Monitoring

```bash
# View system status
ros2 topic echo /vehicle_status

# Check TF tree
ros2 run tf2_tools view_frames

# Monitor specific topics
ros2 topic list
ros2 topic info /odom
```

## Troubleshooting

### TF Errors
- Check that all TF broadcasters are running
- Verify coordinate frames in URDF

### Navigation Issues
- Ensure map is loaded for global localization
- Check costmap layers configuration

### Communication Issues
- Verify all nodes are running: `ros2 node list`
- Check network connectivity for hardware interfaces
