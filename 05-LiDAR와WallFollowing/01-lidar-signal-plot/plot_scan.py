#!/usr/bin/env python3
# plot_scan.py
import math
import matplotlib.pyplot as plt
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class ScanPlotter(Node):
    def __init__(self):
        super().__init__('scan_plotter')
        self.create_subscription(LaserScan, '/scan', self.callback, 10)
        self.done = False

    def callback(self, scan):
        if self.done:
            return
        self.done = True

        angles = [scan.angle_min + i * scan.angle_increment
                  for i in range(len(scan.ranges))]
        ranges = [r if math.isfinite(r) else scan.range_max for r in scan.ranges]
        xs = [r * math.cos(a) for r, a in zip(ranges, angles)]
        ys = [r * math.sin(a) for r, a in zip(ranges, angles)]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        ax1.plot([math.degrees(a) for a in angles], ranges)
        ax1.set_xlabel('각도 (도)')
        ax1.set_ylabel('거리 (m)')
        ax1.set_title('신호로 본 LiDAR: r(θ)')

        ax2.scatter(xs, ys, s=2)
        ax2.set_xlabel('x (m, 전방)')
        ax2.set_ylabel('y (m, 좌측)')
        ax2.set_aspect('equal')
        ax2.set_title('새의 눈 시점: 점군')

        plt.tight_layout()
        plt.savefig('scan_plot.png')
        plt.show()


def main():
    rclpy.init()
    node = ScanPlotter()
    while not node.done:
        rclpy.spin_once(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
