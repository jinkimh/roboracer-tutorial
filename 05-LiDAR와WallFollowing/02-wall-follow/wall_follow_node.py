#!/usr/bin/env python3
# wall_follow_node.py
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDriveStamped

STEERING_LIMIT = 0.4189  # Roboracer 표준 차량의 조향각 한계(rad), 4.4절 참고


class WallFollow(Node):
    def __init__(self):
        super().__init__('wall_follow_node')
        self.declare_parameter('side', 'left')
        self.declare_parameter('desired_distance', 1.0)
        self.declare_parameter('lookahead', 1.0)
        self.declare_parameter('theta_deg', 50.0)
        self.declare_parameter('kp', 1.0)
        self.declare_parameter('ki', 0.0)
        self.declare_parameter('kd', 0.05)
        self.declare_parameter('max_speed', 1.5)
        self.declare_parameter('steering_bias_deg', 0.0)

        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_stamp = None

        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.drive_pub = self.create_publisher(AckermannDriveStamped, '/drive', 10)

    def get_range(self, scan, angle_deg):
        angle_rad = math.radians(angle_deg)
        index = round((angle_rad - scan.angle_min) / scan.angle_increment)
        index = max(0, min(len(scan.ranges) - 1, index))
        r = scan.ranges[index]
        if math.isinf(r) or math.isnan(r):
            r = scan.range_max
        return r

    def scan_callback(self, scan):
        side = self.get_parameter('side').value
        sign = 1.0 if side == 'left' else -1.0
        theta_deg = self.get_parameter('theta_deg').value

        b = self.get_range(scan, 90.0 * sign)
        a = self.get_range(scan, (90.0 - theta_deg) * sign)
        theta = math.radians(theta_deg)

        alpha = math.atan2(a * math.cos(theta) - b, a * math.sin(theta))
        current_distance = b * math.cos(alpha)
        lookahead = self.get_parameter('lookahead').value
        future_distance = current_distance + lookahead * math.sin(alpha)

        desired = self.get_parameter('desired_distance').value
        error = future_distance - desired

        stamp = scan.header.stamp.sec + scan.header.stamp.nanosec * 1e-9
        self.publish_drive(error, sign, stamp)

    def publish_drive(self, error, sign, stamp):
        dt = (stamp - self.prev_stamp) if self.prev_stamp is not None else 0.02
        dt = dt if dt > 0.0 else 1e-3
        self.prev_stamp = stamp

        kp = self.get_parameter('kp').value
        ki = self.get_parameter('ki').value
        kd = self.get_parameter('kd').value

        self.integral = max(-1.0, min(1.0, self.integral + error * dt))
        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        steering = sign * (kp * error + ki * self.integral + kd * derivative)

        # 4.7절의 조향 오프셋 결함을 시뮬레이터에서 재현하기 위한 인위적 편향(기본값 0, 실차에서는
        # 항상 0으로 둠 — 실제 결함은 파라미터가 아니라 서보 자체에 있기 때문).
        bias = math.radians(self.get_parameter('steering_bias_deg').value)
        steering = max(-STEERING_LIMIT, min(STEERING_LIMIT, steering + bias))

        max_speed = self.get_parameter('max_speed').value
        angle_deg = abs(math.degrees(steering))
        if angle_deg < 10.0:
            speed = max_speed
        elif angle_deg < 20.0:
            speed = max_speed * 0.7
        else:
            speed = max_speed * 0.4

        msg = AckermannDriveStamped()
        msg.drive.steering_angle = steering
        msg.drive.speed = speed
        self.drive_pub.publish(msg)


def main():
    rclpy.init()
    rclpy.spin(WallFollow())


if __name__ == '__main__':
    main()
