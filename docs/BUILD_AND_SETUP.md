# AI占位写法 不一定都对 

# Build and Setup Instructions

## Prerequisites (前置要求)

- Ubuntu 22.04 LTS
- ROS 2 Humble
- git
- Python 3.10+
- Docker (optional, for containerized setup)

## System Setup (系统设置)

### 1. Install ROS 2 Humble

```bash
# Add ROS 2 apt repository
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update

# Install ROS 2
sudo apt install ros-humble-desktop

# Source setup file
source /opt/ros/humble/setup.bash
```

### 2. Install Build Tools (安装构建工具)

```bash
sudo apt install -y \
  python3-colcon-common-extensions \
  python3-rosdep \
  build-essential \
  cmake \
  git \
  python3-pip

pip install -U pip setuptools
```

### 3. Clone Workspace (克隆工作区)

```bash
mkdir -p agt_ws/src
cd agt_ws

# Clone AGT Navigation Stack
git clone <repo-url> src/

# Or if already in the src directory:
cd src
```

## Building (构建)

### 1. Install Dependencies (安装依赖)

```bash
cd ~/agt_ws

# Install rosdep dependencies
rosdep update
rosdep install --from-paths src --ignore-src -r -y

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Build Workspace (构建工作区)

```bash
cd ~/agt_ws

# Clean previous builds (optional)
rm -rf build install log

# Build all packages
colcon build --symlink-install

# Or build specific package
colcon build --packages-select package_name --symlink-install
```

### 3. Source Installation (源安装)

```bash
source ~/agt_ws/install/setup.bash

# Add to bashrc for automatic sourcing
echo "source ~/agt_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Docker Setup (Docker设置)

### 1. Build Docker Image (构建Docker镜像)

```bash
cd docker
docker-compose build
```

### 2. Run Container (运行容器)

```bash
# Interactive shell
docker-compose run agt_nav bash

# Or run specific command
docker-compose run agt_nav ros2 launch agt_bringup agt_bringup.launch.xml
```

## Development Setup (开发设置)

### 1. Create New Package (创建新包)

```bash
cd ~/agt_ws/src

# C++ package
ros2 pkg create --build-type ament_cmake new_package

# Python package
ros2 pkg create --build-type ament_python new_package
```

### 2. Run Tests (运行测试)

```bash
cd ~/agt_ws

# Run all tests
colcon test

# Run specific test
colcon test --packages-select package_name
```

### 3. Build Documentation (构建文档)

```bash
# Using rosdoc_lite
rosdoc_lite ~/agt_ws/src/package_name
```

## Troubleshooting (故障排除)

### Build Fails (构建失败)

```bash
# Clean build
rm -rf build install log
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
```

### Missing Dependencies (缺少依赖)

```bash
# Run rosdep again
rosdep install --from-paths src --ignore-src -r -y

# Or manually install
sudo apt install ros-humble-package-name
```

### ROS 2 Not Found (ROS 2未找到)

```bash
# Ensure setup.bash is sourced
source /opt/ros/humble/setup.bash
source ~/agt_ws/install/setup.bash
```

## Verification (验证)

```bash
# Check ROS 2 installation
ros2 --version

# List available packages
ros2 pkg list | grep agt

# Test workspace setup
source ~/agt_ws/install/setup.bash
ros2 run agt_common --version
```

## Next Steps (下一步)

1. Review [Architecture Design](ARCHITECTURE.md)
2. Check [Coordinate Systems](COORDINATE_SYSTEMS.md)
3. Read [Topic Interface](TOPIC_INTERFACE.md)
4. Start with [Quick Start Guide](../README.md#quick-start)
