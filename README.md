# agt_navigation_stack
Navigation system with Ackermann chassis for tomato harvesting robots, supporting autonomous positioning, path planning and obstacle avoidance in agricultural greenhouse environments.

已经将第一版的urdf与阿克曼底盘的can通讯与驱动文件放入

# 第一阶段
    完成基本框架的搭建 讨论正确的框架内容与标准节点话题等的利用
    完成传感器的初始化 正确的车辆外参标定 数据链的时间同步 
    完成阿克曼速度节点的正确转化

    先跑通2D nav2的导航框架与gazebo传感器的正确使用 
    完成测试调试台的gui的测试 能够快速启动节点 组装测试 并显示所有可调的参数保存对应的参数

# 第二阶段
    完成目标能够在rviz中正确显示高精度的urdf模型，也能够使用简化的模型
    前端先用fastlio2算法估计局部位姿，不融合轮速传感器，使用ICP算法进行重定位 实现建图与导航

    swith-nav2模式 使用二维码识别与先验地图上实现稳定路径规划与导航
    改进cartographer算法 在明白其原理后进行前处理 设立实验指标 进行参数优化与实验
     
# 第三阶段
    在传感器数据输入进系统之前做轻量化处理，为数据赋予语义信息，并以此来实现创新
    倾斜安装MID360，通过顶棚和地面的信息做重定位优化

