"""Chassis Bridge - converts cmd_vel to control commands"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from agt_msgs.msg import CtrlCmd
from agt_common.constants import TOPIC_CMD_VEL, TOPIC_CTRL_CMD


class ChassisBridge(Node):
    def __init__(self):
        super().__init__('chassis_bridge')
        
        self.subscription = self.create_subscription(
            Twist,
            TOPIC_CMD_VEL,
            self.cmd_vel_callback,
            10)
        
        self.publisher = self.create_publisher(
            CtrlCmd,
            TOPIC_CTRL_CMD,
            10)
        
        self.get_logger().info('Chassis Bridge initialized')
    
    def cmd_vel_callback(self, msg: Twist):
        """Convert Twist message to CtrlCmd"""
        ctrl_cmd = CtrlCmd()
        
        # Convert m/s to mm/s
        ctrl_cmd.linear_velocity = int(msg.linear.x * 1000)
        # Convert rad/s to 0.01 rad/s
        ctrl_cmd.angular_velocity = int(msg.angular.z * 100)
        
        self.publisher.publish(ctrl_cmd)


def main(args=None):
    rclpy.init(args=args)
    node = ChassisBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
