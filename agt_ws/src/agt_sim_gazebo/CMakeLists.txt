cmake_minimum_required(VERSION 3.16)
project(agt_sim_gazebo)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  launch
  world
  models
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
