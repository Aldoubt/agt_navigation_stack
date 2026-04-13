cmake_minimum_required(VERSION 3.16)
project(agt_driver)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  livox_ros_driver2
  orbbec_sdk
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
