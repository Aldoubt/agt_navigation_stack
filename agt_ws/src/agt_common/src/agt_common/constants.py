"""Common constants and utilities for AGT Navigation Stack"""

# Frame IDs
FRAME_MAP = "map"
FRAME_ODOM = "odom"
FRAME_BASE_LINK = "base_link"
FRAME_LIDAR = "lidar_link"
FRAME_CAMERA = "camera_link"
FRAME_IMU = "imu_link"

# Topic names
TOPIC_CMD_VEL = "cmd_vel"
TOPIC_CTRL_CMD = "ctrl_cmd"
TOPIC_CHASSIS_STATE = "chassis_state"
TOPIC_VEHICLE_STATUS = "vehicle_status"
TOPIC_LOCALIZATION_STATE = "localization_state"
TOPIC_LIDAR_SCAN = "scan"
TOPIC_LIDAR_CLOUD = "cloud"
TOPIC_CAMERA_IMAGE = "image_raw"
TOPIC_IMU_DATA = "imu/data"
TOPIC_ODM_DATA = "odom"

# Service names
SERVICE_START_MAPPING = "start_mapping"
SERVICE_STOP_MAPPING = "stop_mapping"
SERVICE_SAVE_MAP = "save_map"
SERVICE_LOAD_MAP = "load_map"

# Coordinate system constants
COORD_TF_TIMEOUT = 5.0  # seconds
COORD_PRECISION = 0.001  # meters

# Velocity limits
MAX_LINEAR_VELOCITY = 1.5  # m/s
MAX_ANGULAR_VELOCITY = 1.0  # rad/s
MIN_LINEAR_VELOCITY = 0.0  # m/s
MIN_ANGULAR_VELOCITY = 0.0  # rad/s

# Time constants
TIME_SYNC_THRESHOLD = 0.1  # seconds
TIME_STAMP_TIMEOUT = 2.0  # seconds
