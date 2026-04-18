from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    input_topic = LaunchConfiguration("input_topic")
    output_topic = LaunchConfiguration("output_topic")
    publish_odom = LaunchConfiguration("publish_odom")
    output_child = LaunchConfiguration("output_child")

    return LaunchDescription(
        [
            DeclareLaunchArgument("input_topic", default_value="/Odometry"),
            DeclareLaunchArgument("output_topic", default_value="/lio_odom"),
            DeclareLaunchArgument("publish_odom", default_value="true"),
            DeclareLaunchArgument("output_child", default_value="livox_frame"),
            Node(
                package="agt_odometry",
                executable="lio_odom_bridge.py",
                name="fastlio_odom_bridge",
                output="screen",
                parameters=[
                    {
                        "input_topic": input_topic,
                        "output_topic": output_topic,
                        "publish_odom": publish_odom,
                        "expected_input_parent": "camera_init",
                        "expected_input_child": "body",
                        "output_parent": "odom",
                        "output_child": output_child,
                    }
                ],
            ),
        ]
    )
