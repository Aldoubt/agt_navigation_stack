import os.path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    package_path = get_package_share_directory("fast_lio")
    default_rviz_config_path = os.path.join(package_path, "rviz", "fastlio.rviz")
    default_config_file = os.path.join(package_path, "config", "agt_mid360.yaml")

    use_sim_time = LaunchConfiguration("use_sim_time")
    rviz_use = LaunchConfiguration("rviz")
    rviz_cfg = LaunchConfiguration("rviz_cfg")
    config_file = LaunchConfiguration("config_file")
    enable_odom_bridge = LaunchConfiguration("enable_odom_bridge")
    bridge_publish_odom = LaunchConfiguration("bridge_publish_odom")
    bridge_output_child_frame = LaunchConfiguration("bridge_output_child_frame")
    bridge_use_input_stamp = LaunchConfiguration("bridge_use_input_stamp")

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time", default_value="false",
        description="Use simulation clock if true"
    )
    declare_rviz_cmd = DeclareLaunchArgument(
        "rviz", default_value="true",
        description="Use RViz to monitor results"
    )
    declare_rviz_config_path_cmd = DeclareLaunchArgument(
        "rviz_cfg", default_value=default_rviz_config_path,
        description="RViz config file path"
    )
    declare_config_file_cmd = DeclareLaunchArgument(
        "config_file", default_value=default_config_file,
        description="Full path to FAST-LIO config file"
    )
    declare_enable_odom_bridge_cmd = DeclareLaunchArgument(
        "enable_odom_bridge", default_value="true",
        description="Enable FAST-LIO odom bridge (camera_init/body -> odom/base_link)"
    )
    declare_bridge_publish_odom_cmd = DeclareLaunchArgument(
        "bridge_publish_odom", default_value="true",
        description="Publish bridged nav_msgs/Odometry topic (/lio_odom)"
    )
    declare_bridge_output_child_frame_cmd = DeclareLaunchArgument(
        "bridge_output_child_frame", default_value="base_link",
        description="Bridge output child frame. Default is base_link for Nav2 TF chain."
    )
    declare_bridge_use_input_stamp_cmd = DeclareLaunchArgument(
        "bridge_use_input_stamp", default_value="true",
        description="Use input odometry header stamp for bridged odom/tf."
    )

    fast_lio_node = Node(
        package="fast_lio",
        executable="fastlio_mapping",
        parameters=[config_file, {"use_sim_time": use_sim_time}],
        output="screen",
        sigterm_timeout="30",
        sigkill_timeout="60",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_cfg],
        condition=IfCondition(rviz_use)
    )

    odom_bridge_node = Node(
        package="agt_odometry",
        executable="lio_odom_bridge.py",
        name="fastlio_odom_bridge",
        parameters=[{
            "input_topic": "/Odometry",
            "output_topic": "/lio_odom",
            "publish_odom": bridge_publish_odom,
            "expected_input_parent": "camera_init",
            "expected_input_child": "body",
            "output_parent": "odom",
            "output_child": bridge_output_child_frame,
            "use_input_stamp": bridge_use_input_stamp,
        }],
        output="screen",
        condition=IfCondition(enable_odom_bridge)
    )

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_rviz_cmd)
    ld.add_action(declare_rviz_config_path_cmd)
    ld.add_action(declare_config_file_cmd)
    ld.add_action(declare_enable_odom_bridge_cmd)
    ld.add_action(declare_bridge_publish_odom_cmd)
    ld.add_action(declare_bridge_output_child_frame_cmd)
    ld.add_action(declare_bridge_use_input_stamp_cmd)
    ld.add_action(fast_lio_node)
    ld.add_action(odom_bridge_node)
    ld.add_action(rviz_node)
    return ld
