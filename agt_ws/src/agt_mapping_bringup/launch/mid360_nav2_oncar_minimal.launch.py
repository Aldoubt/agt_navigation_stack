import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    mapping_pkg = get_package_share_directory("agt_mapping_bringup")
    yhs_pkg = get_package_share_directory("yhs_can_control")

    map_yaml = LaunchConfiguration("map_yaml")
    nav2_params = LaunchConfiguration("nav2_params")
    use_sim_time = LaunchConfiguration("use_sim_time")
    autostart = LaunchConfiguration("autostart")
    rviz = LaunchConfiguration("rviz")
    rviz_cfg = LaunchConfiguration("rviz_cfg")
    can_params = LaunchConfiguration("can_params")
    twist_to_yhs_params = LaunchConfiguration("twist_to_yhs_params")

    declare_map_yaml = DeclareLaunchArgument(
        "map_yaml",
        default_value="/home/yangxuan/agt_navigation_stack/datasets/fastlio_mid360_map.yaml",
    )
    declare_nav2_params = DeclareLaunchArgument(
        "nav2_params",
        default_value=os.path.join(
            get_package_share_directory("agt_nav2"), "config", "nav2_params.yaml"
        ),
    )
    declare_use_sim_time = DeclareLaunchArgument("use_sim_time", default_value="false")
    declare_autostart = DeclareLaunchArgument("autostart", default_value="true")
    declare_rviz = DeclareLaunchArgument("rviz", default_value="true")
    declare_rviz_cfg = DeclareLaunchArgument(
        "rviz_cfg",
        default_value=os.path.join(
            get_package_share_directory("nav2_bringup"), "rviz", "nav2_default_view.rviz"
        ),
    )
    declare_can_params = DeclareLaunchArgument(
        "can_params", default_value=os.path.join(yhs_pkg, "params", "cfg.yaml")
    )
    declare_twist_to_yhs_params = DeclareLaunchArgument(
        "twist_to_yhs_params",
        default_value=os.path.join(yhs_pkg, "params", "twist_to_yhs_cmd.yaml"),
    )

    nav2_stack = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(mapping_pkg, "launch", "mid360_nav2_minimal.launch.py")
        ),
        launch_arguments={
            "map_yaml": map_yaml,
            "nav2_params": nav2_params,
            "use_sim_time": use_sim_time,
            "autostart": autostart,
            "rviz": rviz,
            "rviz_cfg": rviz_cfg,
        }.items(),
    )

    yhs_can_control = Node(
        package="yhs_can_control",
        executable="yhs_can_control_node",
        name="yhs_can_control_node",
        output="screen",
        parameters=[can_params],
    )

    twist_to_yhs_cmd = Node(
        package="yhs_can_control",
        executable="twist_to_yhs_cmd_node",
        name="twist_to_yhs_cmd_node",
        output="screen",
        parameters=[twist_to_yhs_params],
    )

    ld = LaunchDescription()
    ld.add_action(declare_map_yaml)
    ld.add_action(declare_nav2_params)
    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_autostart)
    ld.add_action(declare_rviz)
    ld.add_action(declare_rviz_cfg)
    ld.add_action(declare_can_params)
    ld.add_action(declare_twist_to_yhs_params)
    ld.add_action(nav2_stack)
    ld.add_action(yhs_can_control)
    ld.add_action(twist_to_yhs_cmd)
    return ld
