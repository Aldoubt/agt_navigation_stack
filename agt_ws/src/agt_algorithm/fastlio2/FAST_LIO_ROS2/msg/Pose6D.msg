# 某一帧中，IMU 测量时刻对应的预积分激光雷达状态
float64  offset_time # 测量相对于首个激光雷达点的时间偏移量
float64[3] acc       # the preintegrated total acceleration (global frame) at the Lidar origin
float64[3] gyr       # the unbiased angular velocity (body frame) at the Lidar origin
float64[3] vel       # the preintegrated velocity (global frame) at the Lidar origin
float64[3] pos       # the preintegrated position (global frame) at the Lidar origin
float64[9] rot       # the preintegrated rotation (global frame) at the Lidar origin