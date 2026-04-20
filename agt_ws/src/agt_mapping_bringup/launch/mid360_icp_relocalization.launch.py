import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    this_pkg = get_package_share_directory("agt_mapping_bringup")
    fast_lio_pkg = get_package_share_directory("fast_lio")
    livox_pkg = get_package_share_directory("livox_ros_driver2")
    icp_pkg = get_package_share_directory("icp_localization_ros2")

    icp_params = LaunchConfiguration("icp_params")
    map_pcd = LaunchConfiguration("map_pcd")
    use_rviz = LaunchConfiguration("rviz")
    rviz_cfg = LaunchConfiguration("rviz_cfg")

    declare_icp_params = DeclareLaunchArgument(
        "icp_params",
        default_value=os.path.join(this_pkg, "config", "icp_reloc_mid360.yaml"),
        description="ICP relocalization parameter file",
    )
    declare_map_pcd = DeclareLaunchArgument(
        "map_pcd",
        default_value="/home/yangxuan/agt_navigation_stack/datasets/fastlio_mid360_map.pcd",
        description="Global map PCD used by ICP",
    )
    declare_rviz = DeclareLaunchArgument("rviz", default_value="true")
    declare_rviz_cfg = DeclareLaunchArgument(
        "rviz_cfg",
        default_value=os.path.join(fast_lio_pkg, "rviz", "fastlio.rviz"),
    )

    livox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(livox_pkg, "launch_ROS2", "msg_MID360_launch.py")
        )
    )

    fastlio_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(fast_lio_pkg, "launch", "agt_mid360.launch.py")
        ),
        launch_arguments={
            "rviz": "false",
            "enable_odom_bridge": "true",
            "bridge_publish_odom": "true",
            "bridge_output_child_frame": "base_link",
        }.items(),
    )

    icp_node = Node(
        package="icp_localization_ros2",
        executable="icp_localization",
        name="icp_localization",
        output="screen",
        parameters=[
            icp_params,
            {
                "pcd_file_path": map_pcd,
                "icp_config_path": os.path.join(icp_pkg, "config", "icp.yaml"),
                "input_filters_config_path": "config/input_filters_mid360.yaml",
            },
        ],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_cfg],
        condition=IfCondition(use_rviz),
    )

    ld = LaunchDescription()
    ld.add_action(declare_icp_params)
    ld.add_action(declare_map_pcd)
    ld.add_action(declare_rviz)
    ld.add_action(declare_rviz_cfg)
    ld.add_action(livox_launch)
    ld.add_action(fastlio_launch)
    ld.add_action(icp_node)
    ld.add_action(rviz_node)
    return ld
