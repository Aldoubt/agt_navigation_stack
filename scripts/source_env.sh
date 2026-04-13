#!/bin/bash
# Source script for setting up AGT environment

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE="${SCRIPT_DIR}/agt_ws"

# Source ROS 2
source /opt/ros/humble/setup.bash

# Source workspace
source "$WORKSPACE"/install/setup.bash

echo "AGT Navigation Stack environment loaded"
echo "Workspace: $WORKSPACE"
echo "ROS_DOMAIN_ID: $ROS_DOMAIN_ID"
