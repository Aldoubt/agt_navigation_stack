FROM ros:humble

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    python3-colcon-common-extensions \
    python3-flake8 \
    python3-mypy \
    python3-pytest \
    python3-pytest-cov \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox \
    ros-humble-cartographer \
    ros-humble-cartographer-ros \
    liblivox-ros-driver2 \
    && rm -rf /var/lib/apt/lists/*

# Create workspace
WORKDIR /root/agt_ws

# Copy source code
COPY . .

# Build workspace
RUN . /opt/ros/humble/setup.sh && \
    rosdep install --from-paths src --ignore-src -r -y && \
    colcon build --symlink-install

# Setup entry point
RUN echo "source /root/agt_ws/install/setup.bash" >> ~/.bashrc

ENTRYPOINT ["/bin/bash"]
