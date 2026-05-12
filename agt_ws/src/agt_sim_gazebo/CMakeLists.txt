cmake_minimum_required(VERSION 3.16)
project(agt_sim_gazebo)

find_package(ament_cmake REQUIRED)

set(_install_dirs "")

foreach(dir launch world models)
  if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${dir}")
    list(APPEND _install_dirs "${dir}")
  endif()
endforeach()

if(_install_dirs)
  install(DIRECTORY
    ${_install_dirs}
    DESTINATION share/${PROJECT_NAME}/
  )
endif()

ament_package()
