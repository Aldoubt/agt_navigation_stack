cmake_minimum_required(VERSION 3.16)
project(agt_msgs)

find_package(ament_cmake REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  msg/CtrlCmd.msg
  msg/ChassisState.msg
  msg/VehicleStatus.msg
  msg/LocalizationState.msg
  DEPENDENCIES
  builtin_interfaces
  geometry_msgs
  sensor_msgs
)

ament_package()
