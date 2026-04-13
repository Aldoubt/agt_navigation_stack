
Core Navigation Topics

/cmd_vel
  type: geometry_msgs/Twist
  source: nav2_controller
  note: generic navigation velocity command, not chassis-native ackermann command

/ctrl_cmd
  type: agt_msgs/CtrlCmd
  source: agt_chassis_bridge
  note: ackermann executable command

/cloud_raw
  type: sensor_msgs/PointCloud2
  source: livox_driver

/cloud_filtered
  type: sensor_msgs/PointCloud2
  source: agt_sensor_proc

/scan
  type: sensor_msgs/LaserScan
  source: cloud_to_scan projector
  note: for 2D costmap / 2D localization

/odom
  type: nav_msgs/Odometry
  source: agt_odometry
  note: represents odom -> base_link

/tf
  odom -> base_link: agt_odometry
  map -> odom: agt_location

/localization_state
  type: agt_msgs/LocalizationState
  source: agt_location
  note: summary for GUI / mission, not TF replacement