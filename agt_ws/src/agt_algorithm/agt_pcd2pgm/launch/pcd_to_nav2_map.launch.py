import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    config_file = LaunchConfiguration("config_file")

    declare_config_file_cmd = DeclareLaunchArgument(
        "config_file",
        default_value=os.path.join(
            get_package_share_directory("agt_pcd2pgm"),
            "config",
            "config_pcd2pgm.yaml",
        ),
        description="YAML config file for agt_pcd2pgm",
    )

    pcd_to_nav2_map_node = Node(
        package="agt_pcd2pgm",
        executable="agt_pcd2pgm_node",
        output="screen",
        parameters=[config_file],
    )

    return LaunchDescription([
        declare_config_file_cmd,
        pcd_to_nav2_map_node,
    ])
