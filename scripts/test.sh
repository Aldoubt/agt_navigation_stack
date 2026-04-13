#!/bin/bash
# Run tests for AGT Navigation Stack

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE="${SCRIPT_DIR}/../agt_ws"

cd "$WORKSPACE"

source /opt/ros/humble/setup.bash
source install/setup.bash

echo "Running AGT Navigation Stack tests..."
echo ""

colcon test --packages-ignore gazebo_ros_pkgs

# Print test results
echo ""
echo "Test Summary:"
colcon test-result --all
