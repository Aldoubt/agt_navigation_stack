#!/bin/bash
# Setup script for AGT Navigation Stack development environment

set -e

echo "================================"
echo "AGT Navigation Stack Setup"
echo "================================"

# Check if ROS 2 is installed
if [ ! -d "/opt/ros/humble" ]; then
    echo "Error: ROS 2 Humble not found. Please install ROS 2 first."
    exit 1
fi

# Source ROS 2
source /opt/ros/humble/setup.bash
echo "✓ ROS 2 Humble sourced"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE="${SCRIPT_DIR}/agt_ws"

# Build workspace
cd "$WORKSPACE"

echo ""
echo "Installing rosdep dependencies..."
rosdep install --from-paths src --ignore-src -r -y

echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Building workspace..."
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "To use the workspace, run:"
echo "  source $WORKSPACE/install/setup.bash"
echo ""
echo "To launch the system, run:"
echo "  ros2 launch agt_bringup agt_bringup.launch.xml"
echo ""
