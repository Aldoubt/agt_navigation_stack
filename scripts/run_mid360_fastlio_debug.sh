#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SETUP_BASH="${ROOT_DIR}/install/setup.bash"
RVIZ_CFG="${ROOT_DIR}/agt_ws/src/agt_algorithm/fastlio2/FAST_LIO_ROS2/rviz/fastlio.rviz"

if [[ ! -f "${SETUP_BASH}" ]]; then
  echo "[ERROR] ${SETUP_BASH} not found."
  echo "Please run: colcon build"
  exit 1
fi

CMD_DRIVER="source '${SETUP_BASH}' && export ROS_LOG_DIR=/tmp/ros_logs && ros2 launch livox_ros_driver2 msg_MID360_launch.py"
CMD_FASTLIO="source '${SETUP_BASH}' && export ROS_LOG_DIR=/tmp/ros_logs && ros2 launch fast_lio agt_mid360.launch.py rviz:=false"
CMD_CHECK="source '${SETUP_BASH}' && export ROS_LOG_DIR=/tmp/ros_logs && \
echo '=== livox topics ===' && ros2 topic hz /livox/lidar && \
echo '=== imu topics ===' && ros2 topic hz /livox/imu && \
echo '=== fast-lio odom ===' && ros2 topic echo /Odometry --once && \
echo '=== bridge odom ===' && ros2 topic echo /lio_odom --once && \
echo '=== tf odom->livox_frame ===' && ros2 run tf2_ros tf2_echo odom livox_frame"
CMD_RVIZ="source '${SETUP_BASH}' && export ROS_LOG_DIR=/tmp/ros_logs && rviz2 -d '${RVIZ_CFG}'"

open_tab() {
  local title="$1"
  local cmd="$2"
  gnome-terminal --title="${title}" -- bash -lc "${cmd}; exec bash"
}

echo "[INFO] Workspace: ${ROOT_DIR}"
echo "[INFO] Starting MID360 + FAST-LIO debug sessions..."

if command -v gnome-terminal >/dev/null 2>&1; then
  open_tab "MID360_DRIVER" "${CMD_DRIVER}"
  sleep 1
  open_tab "FASTLIO_BRIDGE" "${CMD_FASTLIO}"
  sleep 1
  open_tab "CHECK_TOPICS_TF" "${CMD_CHECK}"
  sleep 1
  open_tab "RVIZ_FASTLIO" "${CMD_RVIZ}"
  echo "[INFO] 4 terminals opened."
  exit 0
fi

if command -v tmux >/dev/null 2>&1; then
  SESSION="mid360_fastlio_debug"
  tmux new-session -d -s "${SESSION}" "bash -lc \"${CMD_DRIVER}\""
  tmux split-window -h "bash -lc \"${CMD_FASTLIO}\""
  tmux split-window -v "bash -lc \"${CMD_CHECK}\""
  tmux select-pane -t 0
  tmux split-window -v "bash -lc \"${CMD_RVIZ}\""
  tmux select-layout tiled >/dev/null 2>&1 || true
  echo "[INFO] tmux session '${SESSION}' started. Attach with:"
  echo "tmux attach -t ${SESSION}"
  exit 0
fi

cat <<EOF
[WARN] Neither gnome-terminal nor tmux found.
Run these commands manually in 4 terminals:

[1] Driver:
${CMD_DRIVER}

[2] FAST-LIO + bridge:
${CMD_FASTLIO}

[3] Checks:
${CMD_CHECK}

[4] RViz:
${CMD_RVIZ}
EOF
