#!/usr/bin/env python3
# commander_node.py
import math
import rclpy
from rclpy.node import Node
from keyboard_msgs.msg import Key
from ackermann_msgs.msg import AckermannDriveStamped

K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE = 273, 274, 276, 275, 32

class Commander(Node):
    def __init__(self):
        super().__init__('keyboard_commander')
        self.declare_parameter('speed_forward', 1.0)
        self.declare_parameter('speed_reverse', -0.5)
        self.declare_parameter('steer_angle_deg', 20.0)
        self.drive_pub = self.create_publisher(AckermannDriveStamped, '/drive', 10)
        self.create_subscription(Key, '/keydown', self.key_callback, 10)

    def key_callback(self, key_msg):
        speed_fwd = self.get_parameter('speed_forward').value
        speed_rev = self.get_parameter('speed_reverse').value
        steer = math.radians(self.get_parameter('steer_angle_deg').value)

        msg = AckermannDriveStamped()
        if key_msg.code == K_UP:
            msg.drive.speed = speed_fwd
        elif key_msg.code == K_DOWN:
            msg.drive.speed = speed_rev
        elif key_msg.code == K_LEFT:
            msg.drive.speed = speed_fwd * 0.6
            msg.drive.steering_angle = steer
        elif key_msg.code == K_RIGHT:
            msg.drive.speed = speed_fwd * 0.6
            msg.drive.steering_angle = -steer
        elif key_msg.code == K_SPACE:
            msg.drive.speed = 0.0
        else:
            return

        self.drive_pub.publish(msg)
        self.get_logger().info(
            f'speed={msg.drive.speed:.2f} m/s, steer={msg.drive.steering_angle:.2f} rad')

def main():
    rclpy.init()
    rclpy.spin(Commander())

if __name__ == '__main__':
    main()
