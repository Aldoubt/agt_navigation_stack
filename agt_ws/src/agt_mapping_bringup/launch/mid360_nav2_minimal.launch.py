import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    mapping_pkg = get_package_share_directory("agt_mapping_bringup")
    nav2_pkg = get_package_share_directory("agt_nav2")
    desc_pkg = get_package_share_directory("agt_acm_description")
    nav2_bringup_pkg = get_package_share_directory("nav2_bringup")

    map_yaml = LaunchConfiguration("map_yaml")
    nav2_params = LaunchConfiguration("nav2_params")
    use_sim_time = LaunchConfiguration("use_sim_time")
    autostart = LaunchConfiguration("autostart")
    rviz = LaunchConfiguration("rviz")
    rviz_cfg = LaunchConfiguration("rviz_cfg")

    default_map_yaml = "/home/yangxuan/agt_navigation_stack/datasets/fastlio_mid360_map.yaml"
    default_nav2_params = os.path.join(nav2_pkg, "config", "nav2_params.yaml")
    default_map_server_params = os.path.join(mapping_pkg, "config", "map_server.yaml")
    default_rviz_cfg = os.path.join(nav2_bringup_pkg, "rviz", "nav2_default_view.rviz")
    urdf_path = os.path.join(desc_pkg, "urdf", "agt_robot.urdf")

    declare_map_yaml = DeclareLaunchArgument("map_yaml", default_value=default_map_yaml)
    declare_nav2_params = DeclareLaunchArgument(
        "nav2_params", default_value=default_nav2_params
    )
    declare_use_sim_time = DeclareLaunchArgument("use_sim_time", default_value="false")
    declare_autostart = DeclareLaunchArgument("autostart", default_value="true")
    declare_rviz = DeclareLaunchArgument("rviz", default_value="false")
    declare_rviz_cfg = DeclareLaunchArgument("rviz_cfg", default_value=default_rviz_cfg)

    # Existing localization chain: livox + FAST-LIO + bridge + ICP(map->odom).
    localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(mapping_pkg, "launch", "mid360_icp_relocalization.launch.py")
        ),
        launch_arguments={"rviz": "false"}.items(),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "robot_description": ParameterValue(
                    Command([FindExecutable(name="xacro"), " ", urdf_path]),
                    value_type=str,
                ),
            }
        ],
    )

    map_server = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[
            default_map_server_params,
            {"yaml_filename": map_yaml, "use_sim_time": use_sim_time},
        ],
    )

    lifecycle_manager_map = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_map",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "autostart": autostart,
                "node_names": ["map_server"],
            }
        ],
    )

    nav2_navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_pkg, "launch", "navigation_launch.py")
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "autostart": autostart,
            "params_file": nav2_params,
            "use_composition": "False",
        }.items(),
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_cfg],
        output="screen",
        condition=IfCondition(rviz),
    )

    ld = LaunchDescription()
    ld.add_action(declare_map_yaml)
    ld.add_action(declare_nav2_params)
    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_autostart)
    ld.add_action(declare_rviz)
    ld.add_action(declare_rviz_cfg)
    ld.add_action(localization_launch)
    ld.add_action(robot_state_publisher)
    ld.add_action(map_server)
    ld.add_action(lifecycle_manager_map)
    ld.add_action(nav2_navigation)
    ld.add_action(rviz_node)
    return ld
