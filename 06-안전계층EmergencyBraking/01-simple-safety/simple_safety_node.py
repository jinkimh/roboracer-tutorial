#!/usr/bin/env python3
# simple_safety_node.py
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from ackermann_msgs.msg import AckermannDriveStamped


class SimpleSafetyNode(Node):
    def __init__(self):
        super().__init__('simple_safety_node')
        self.declare_parameter('odom_topic', '/ego_racecar/odom')
        self.declare_parameter('desired_speed', 2.0)
        self.declare_parameter('fov_deg', 10.0)
        self.declare_parameter('ttc_threshold', 0.8)
        self.declare_parameter('reverse_ttc_offset', 0.8)

        self.speed = 0.0
        self.desired_speed = self.get_parameter('desired_speed').value

        odom_topic = self.get_parameter('odom_topic').value
        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.create_subscription(Odometry, odom_topic, self.odom_callback, 10)
        self.drive_pub = self.create_publisher(AckermannDriveStamped, '/drive', 10)

    def odom_callback(self, odom_msg):
        self.speed = odom_msg.twist.twist.linear.x

    def min_ttc_in_fov(self, scan):
        fov = math.radians(self.get_parameter('fov_deg').value)
        i_min = max(0, round((-fov - scan.angle_min) / scan.angle_increment))
        i_max = min(len(scan.ranges) - 1, round((fov - scan.angle_min) / scan.angle_increment))

        min_ttc = 60.0
        for i in range(i_min, i_max + 1):
            r = scan.ranges[i]
            if math.isinf(r) or math.isnan(r):
                continue
            angle = scan.angle_min + i * scan.angle_increment
            r_dot = self.speed * math.cos(angle)
            ttc = min(max(r / max(r_dot, 0.001), 0.0), 60.0)
            min_ttc = min(min_ttc, ttc)
        return min_ttc

    def scan_callback(self, scan):
        min_ttc = self.min_ttc_in_fov(scan)
        thres = self.get_parameter('ttc_threshold').value
        reverse_offset = self.get_parameter('reverse_ttc_offset').value

        if (self.speed > 0.0 and min_ttc < thres) or \
           (self.speed < 0.0 and min_ttc < thres + reverse_offset):
            self.get_logger().warn(f'TTC {min_ttc:.2f}s — 긴급 제동(복구 없음)')
            self.desired_speed = 0.0

        msg = AckermannDriveStamped()
        msg.drive.steering_angle = 0.0
        msg.drive.speed = self.desired_speed
        self.drive_pub.publish(msg)


def main():
    rclpy.init()
    rclpy.spin(SimpleSafetyNode())


if __name__ == '__main__':
    main()
