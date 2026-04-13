# Message and service types for AGT Navigation Stack

## CtrlCmd.msg - Control Command
# Unified control command for the chassis
### Fields
- int32 linear_velocity       # Linear velocity in mm/s
- int32 angular_velocity      # Angular velocity in 0.01 rad/s
- uint8 time_stamp            # Timestamp for synchronization

## ChassisState.msg - Chassis State
# Current state of the chassis
### Fields
- float64 odom_x              # Odometry X position (m)
- float64 odom_y              # Odometry Y position (m)
- float64 odom_theta          # Odometry orientation (rad)
- float64 linear_velocity     # Current linear velocity (m/s)
- float64 angular_velocity    # Current angular velocity (rad/s)

## VehicleStatus.msg - Vehicle Status
# Overall vehicle operational status
### Fields
- uint8 battery_level         # Battery level (0-100%)
- uint8 error_code            # Error code
- bool is_moving              # Is vehicle moving
- builtin_interfaces/Time update_time  # Last update time

## LocalizationState.msg - Localization State
# Global localization state
### Fields
- geometry_msgs/PoseWithCovariance pose  # Global pose
- geometry_msgs/TwistWithCovariance velocity # Velocity with covariance
- uint8 confidence            # Localization confidence (0-100%)
- string frame_id             # Reference frame
