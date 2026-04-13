"""Odometry estimation node"""

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import numpy as np


class OdometryEstimator(Node):
    def __init__(self):
        super().__init__('odometry_node')
        
        self.tf_broadcaster = TransformBroadcaster(self)
        
        self.publisher = self.create_publisher(
            Odometry,
            'odom',
            10)
        
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        self.get_logger().info('Odometry Estimator initialized')
    
    def publish_odometry(self):
        """Publish odometry data"""
        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"
        
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        
        self.publisher.publish(odom)


def main(args=None):
    rclpy.init(args=args)
    node = OdometryEstimator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
