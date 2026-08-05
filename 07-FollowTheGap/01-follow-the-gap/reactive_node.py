#!/usr/bin/env python3
# reactive_node.py
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDriveStamped

STEERING_LIMIT = 0.4189  # Roboracer 표준 차량의 조향각 한계(rad), 4.4절 참고


class ReactiveFollowGap(Node):
    def __init__(self):
        super().__init__('reactive_node')
        self.declare_parameter('max_range', 4.0)
        self.declare_parameter('fov_deg', 180.0)
        self.declare_parameter('bubble_radius_beams', 20)
        self.declare_parameter('v_min', 0.5)
        self.declare_parameter('v_max', 3.0)

        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.drive_pub = self.create_publisher(AckermannDriveStamped, '/drive', 10)

    def preprocess(self, scan):
        max_range = self.get_parameter('max_range').value
        ranges = []
        for r in scan.ranges:
            if math.isinf(r) or math.isnan(r):
                r = max_range
            ranges.append(min(r, max_range))
        return ranges

    def fov_bounds(self, scan):
        fov = math.radians(self.get_parameter('fov_deg').value)
        i_min = max(0, round((-fov / 2 - scan.angle_min) / scan.angle_increment))
        i_max = min(len(scan.ranges) - 1, round((fov / 2 - scan.angle_min) / scan.angle_increment))
        return i_min, i_max

    def apply_bubble(self, window):
        closest_i = min(range(len(window)), key=lambda i: window[i])
        radius = self.get_parameter('bubble_radius_beams').value
        lo = max(0, closest_i - radius)
        hi = min(len(window), closest_i + radius + 1)
        for i in range(lo, hi):
            window[i] = 0.0
        return window

    def find_max_gap(self, window):
        best_start, best_len, start = 0, 0, None
        for i, r in enumerate(window):
            if r > 0.0:
                if start is None:
                    start = i
                if i - start + 1 > best_len:
                    best_len = i - start + 1
                    best_start = start
            else:
                start = None
        return best_start, best_start + best_len  # [start, end)

    def scan_callback(self, scan):
        ranges = self.preprocess(scan)
        i_min, i_max = self.fov_bounds(scan)
        window = self.apply_bubble(ranges[i_min:i_max + 1])
        start, end = self.find_max_gap(window)

        if end <= start:
            self.publish_drive(0.0, 0.0)
            return

        best_i = i_min + (start + end - 1) // 2
        angle = scan.angle_min + best_i * scan.angle_increment
        steering = max(-STEERING_LIMIT, min(STEERING_LIMIT, angle))

        v_min = self.get_parameter('v_min').value
        v_max = self.get_parameter('v_max').value
        k = (v_max - v_min) / STEERING_LIMIT
        speed = max(v_min, min(v_max, v_max - k * abs(steering)))

        self.publish_drive(steering, speed)

    def publish_drive(self, steering, speed):
        msg = AckermannDriveStamped()
        msg.drive.steering_angle = steering
        msg.drive.speed = speed
        self.drive_pub.publish(msg)


def main():
    rclpy.init()
    rclpy.spin(ReactiveFollowGap())


if __name__ == '__main__':
    main()
