# agt_navigation_stack

专门为AgroTech智能机械协会的同学提供一套标准的开发框架，提高开发与学习的效率

AGT_navigation_stack/
├── .github/ github平台相关的配置文件目录
├── docs/  系统文档目录 包括整机架构设计与坐标系定义 TF树说明相关内容 topic接口说明
           包依赖关系 开发规范 硬件接线说明 测试验证流程 
├── specs/ 接口规范目录 
├── scripts/ 脚本目录 辅助脚本 
├── tools/ 开发与调试工具目录
├── docker/ 环境复现目录
├── third_party/ 第三方依赖说明与包装目录 放.repos文件 patch 封装说明 版本锁定说明
├── datasets/    数据资产目录 小型测试数据 示例地图 参数测试基准数据 数据说明
                 最好能固定一份固定测试的数据集
├── agt_ws/src

    /agt_acm_description 机器人描述层

    /agt_algorithm 算法隔离层 
        / fastlio2
        / RTAB-Map
        / ORB-SLAM 3
        / 

    /agt_bringup 全系统编排层
        实车、建图、定位、导航、仿真、模式切换总launch   
        
    /agt_chassis_base 底盘基础通信层
        /yhs_can_ctrl
        /yhs_can_interfaces
        agt_ws/src/agt_chassis_base/使用说明.doc

    /agt_chassis_bridge 控制桥接层
        输入/cmd_vel
        输出/ctrl_cmd
        
    /agt_common 全项目通用基础库 （GPT说要就放上来了）
        坐标系字符串常量
        topic名称常量

    /agt_driver 传感器驱动层
        /livox_ros_driver2 放雷达专用的launch 设备连接参数 基础驱动说明文档
        /ORBBEC SDK 奥比中光相机驱动层

    /agt_location 全局定位层 map -> odom 输出/localization_state
        /icp_relocalization
        /amcl
        /RTAB-Map localization mode
        /rtk-location
        /airdrop QR基于先验地图的重定位模式
        其他全局定位接口

    /agt_mapping_bringup 建图启动层
        不同版本的建图模式的launch文件

    /agt_mission 任务与状态机层 
        
    /agt_msgs 统一的消息接口定义 
        ctrlcmd.msg
        chassisState.msg
        VehicleStatus.msg
        LocalizationState.msg
        
    /agt_nav2 导航配置层
        输入/tf /scan 或 PointCloud2
        map，odom
        nav2_params.yaml
        planner 参数 
        controller 参数 
        costmap 参数 
        behavior tree xml 
        map_server 配置

    /agt_odometry 连续运动估计层  odom → base_link
        ekf、ukf等对数据进行处理与滤波
        
        
    /agt_sensor_proc 传感器预处理层
        /点云滤波 减少杂波的影响
        /IMU滤波 减少零漂与温漂的影响
        /多传感器时间戳输出与数据质量的同步检查

        
    /agt_sim_gazebo gazebo仿真环境的配置与使用
        /world
        /

    /agt_tools_gui 工具与可视化层 参数控制台 + 状态仪表盘 + 实验记录面板
        参数面板 
        预设保存/加载 
        调试 GUI 
        topic 监控 
        TF 可视化辅助 
        地图资产管理辅助



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

