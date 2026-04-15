cmake_minimum_required(VERSION 3.16)
project(agt_mission)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

ament_python_install_package(${PROJECT_NAME}
  PACKAGE_DIR src/${PROJECT_NAME}
)

set(_install_dirs "")

foreach(dir launch config)
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
