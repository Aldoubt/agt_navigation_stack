#!/usr/bin/env python3
"""Bridge FAST-LIO odometry frames (camera_init/body) to odom/base_link."""

import rclpy
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from tf2_ros import TransformBroadcaster


class FastLioOdomBridge(Node):
    def __init__(self) -> None:
        super().__init__("fastlio_odom_bridge")

        self.input_topic = self.declare_parameter("input_topic", "/Odometry").value
        self.output_topic = self.declare_parameter("output_topic", "/lio_odom").value
        self.publish_odom = self.declare_parameter("publish_odom", True).value

        self.expected_input_parent = self.declare_parameter(
            "expected_input_parent", "camera_init"
        ).value
        self.expected_input_child = self.declare_parameter(
            "expected_input_child", "body"
        ).value
        self.output_parent = self.declare_parameter("output_parent", "odom").value
        # FAST-LIO publishes child_frame_id as "body". For Nav2 compatibility
        # we bridge this to odom->base_link and keep lidar_mount from URDF.
        self.output_child = self.declare_parameter("output_child", "base_link").value
        # If false, stamp bridged odom/tf with current ROS time to avoid
        # TF_OLD_DATA when upstream sensor timestamps jump backwards.
        self.use_input_stamp = self.declare_parameter("use_input_stamp", False).value
        self._last_stamp_ns = 0

        self.tf_broadcaster = TransformBroadcaster(self)
        self.sub = self.create_subscription(Odometry, self.input_topic, self.cb, 50)
        self.pub = None
        if self.publish_odom:
            self.pub = self.create_publisher(Odometry, self.output_topic, 50)

        self.get_logger().info(
            f"FAST-LIO odom bridge started: {self.input_topic} "
            f"({self.expected_input_parent}->{self.expected_input_child}) -> "
            f"{self.output_parent}->{self.output_child}, "
            f"publish_odom={self.publish_odom}, output_topic={self.output_topic}"
        )

    def cb(self, msg: Odometry) -> None:
        if (
            msg.header.frame_id != self.expected_input_parent
            or msg.child_frame_id != self.expected_input_child
        ):
            self.get_logger().warn(
                "Input frame mismatch: got "
                f"{msg.header.frame_id}->{msg.child_frame_id}, expected "
                f"{self.expected_input_parent}->{self.expected_input_child}",
                throttle_duration_sec=5.0,
            )

        if self.use_input_stamp:
            stamp_msg = msg.header.stamp
            stamp_ns = int(stamp_msg.sec) * 1_000_000_000 + int(stamp_msg.nanosec)
            # Guarantee strictly monotonic output stamp.
            if stamp_ns <= self._last_stamp_ns:
                stamp_ns = self._last_stamp_ns + 1
                sec = stamp_ns // 1_000_000_000
                nsec = stamp_ns % 1_000_000_000
                stamp_msg.sec = int(sec)
                stamp_msg.nanosec = int(nsec)
                self.get_logger().warn(
                    "Detected non-monotonic input odom stamp; adjusted to preserve TF order.",
                    throttle_duration_sec=5.0,
                )
        else:
            now = self.get_clock().now().to_msg()
            stamp_msg = now
            stamp_ns = int(now.sec) * 1_000_000_000 + int(now.nanosec)

        self._last_stamp_ns = stamp_ns

        tf_msg = TransformStamped()
        tf_msg.header.stamp = stamp_msg
        tf_msg.header.frame_id = self.output_parent
        tf_msg.child_frame_id = self.output_child
        tf_msg.transform.translation.x = msg.pose.pose.position.x
        tf_msg.transform.translation.y = msg.pose.pose.position.y
        tf_msg.transform.translation.z = msg.pose.pose.position.z
        tf_msg.transform.rotation = msg.pose.pose.orientation
        self.tf_broadcaster.sendTransform(tf_msg)

        if self.pub is not None:
            out = Odometry()
            out.header = msg.header
            out.header.stamp = stamp_msg
            out.header.frame_id = self.output_parent
            out.child_frame_id = self.output_child
            out.pose = msg.pose
            out.twist = msg.twist
            self.pub.publish(out)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = FastLioOdomBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    try:
        if rclpy.ok():
            rclpy.shutdown()
    except Exception:
        pass


if __name__ == "__main__":
    main()
