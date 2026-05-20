import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.conditions import IfCondition
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
    rviz_software_gl = LaunchConfiguration("rviz_software_gl")
    enable_robot_state_publisher = LaunchConfiguration("enable_robot_state_publisher")
    auto_enable_io = LaunchConfiguration("auto_enable_io")
    io_enable_rate_hz = LaunchConfiguration("io_enable_rate_hz")
    can_params = LaunchConfiguration("can_params")
    twist_to_yhs_params = LaunchConfiguration("twist_to_yhs_params")

    declare_map_yaml = DeclareLaunchArgument(
        "map_yaml",
        default_value="/home/yangxuan/agt_navigation_stack/datasets/fastlio_mid360_map_dense_manual.yaml",
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
        default_value=os.path.join(mapping_pkg, "config", "nav2_icp_debug.rviz"),
    )
    declare_rviz_software_gl = DeclareLaunchArgument(
        "rviz_software_gl",
        default_value="false",
        description="Use software OpenGL for RViz (fallback for incompatible GPU drivers).",
    )
    declare_enable_robot_state_publisher = DeclareLaunchArgument(
        "enable_robot_state_publisher",
        default_value="false",
        description="Publish URDF TF tree via robot_state_publisher.",
    )
    declare_auto_enable_io = DeclareLaunchArgument(
        "auto_enable_io",
        default_value="false",
        description="Continuously publish /io_cmd with io_cmd_enable=true for chassis enable.",
    )
    declare_io_enable_rate_hz = DeclareLaunchArgument(
        "io_enable_rate_hz",
        default_value="2.0",
        description="Publish rate for auto IO enable publisher.",
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
            "rviz": "false",
            "rviz_cfg": rviz_cfg,
            "enable_robot_state_publisher": enable_robot_state_publisher,
        }.items(),
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_cfg],
        output="screen",
        additional_env={"LIBGL_ALWAYS_SOFTWARE": rviz_software_gl},
        condition=IfCondition(rviz),
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

    auto_io_enable_pub = ExecuteProcess(
        cmd=[
            "ros2",
            "topic",
            "pub",
            "/io_cmd",
            "yhs_can_interfaces/msg/IoCmd",
            "{io_cmd_enable: true, io_cmd_lower_beam_headlamp: false, io_cmd_upper_beam_headlamp: false, io_cmd_turn_lamp: 0, io_cmd_braking_lamp: false, io_cmd_clearance_lamp: false, io_cmd_fog_lamp: false, io_cmd_speaker: false, io_cmd_dis_charge: false}",
            "-r",
            io_enable_rate_hz,
        ],
        output="log",
        condition=IfCondition(auto_enable_io),
    )

    ld = LaunchDescription()
    ld.add_action(declare_map_yaml)
    ld.add_action(declare_nav2_params)
    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_autostart)
    ld.add_action(declare_rviz)
    ld.add_action(declare_rviz_cfg)
    ld.add_action(declare_rviz_software_gl)
    ld.add_action(declare_enable_robot_state_publisher)
    ld.add_action(declare_auto_enable_io)
    ld.add_action(declare_io_enable_rate_hz)
    ld.add_action(declare_can_params)
    ld.add_action(declare_twist_to_yhs_params)
    ld.add_action(rviz_node)
    ld.add_action(nav2_stack)
    ld.add_action(yhs_can_control)
    ld.add_action(twist_to_yhs_cmd)
    ld.add_action(auto_io_enable_pub)
    return ld
