# Install script for directory: /home/admin/catkin_ws/src/carlike_robot_sim/calf_carlike_robot/teb_local_planner_tutorials-kinetic

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/admin/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/admin/catkin_ws/build/carlike_robot_sim/calf_carlike_robot/teb_local_planner_tutorials-kinetic/catkin_generated/installspace/teb_local_planner_tutorials.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/teb_local_planner_tutorials/cmake" TYPE FILE FILES
    "/home/admin/catkin_ws/build/carlike_robot_sim/calf_carlike_robot/teb_local_planner_tutorials-kinetic/catkin_generated/installspace/teb_local_planner_tutorialsConfig.cmake"
    "/home/admin/catkin_ws/build/carlike_robot_sim/calf_carlike_robot/teb_local_planner_tutorials-kinetic/catkin_generated/installspace/teb_local_planner_tutorialsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/teb_local_planner_tutorials" TYPE FILE FILES "/home/admin/catkin_ws/src/carlike_robot_sim/calf_carlike_robot/teb_local_planner_tutorials-kinetic/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/teb_local_planner_tutorials" TYPE DIRECTORY FILES
    "/home/admin/catkin_ws/src/carlike_robot_sim/calf_carlike_robot/teb_local_planner_tutorials-kinetic/launch"
    "/home/admin/catkin_ws/src/carlike_robot_sim/calf_carlike_robot/teb_local_planner_tutorials-kinetic/cfg"
    "/home/admin/catkin_ws/src/carlike_robot_sim/calf_carlike_robot/teb_local_planner_tutorials-kinetic/maps"
    "/home/admin/catkin_ws/src/carlike_robot_sim/calf_carlike_robot/teb_local_planner_tutorials-kinetic/stage"
    "/home/admin/catkin_ws/src/carlike_robot_sim/calf_carlike_robot/teb_local_planner_tutorials-kinetic/scripts"
    REGEX "/\\.svn$" EXCLUDE)
endif()

