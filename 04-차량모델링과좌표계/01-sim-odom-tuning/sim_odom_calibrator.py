#!/usr/bin/env python3
# sim_odom_calibrator.py
import math
import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped, Quaternion

# "실제 VESC 하드웨어"라면 아무도 모르는 값입니다 — 이 실습에서는 정답을
# 코드 안에 숨겨두고, 파라미터 튜닝으로 이 값에 얼마나 가까워지는지 비교합니다.
HIDDEN_ERPM_GAIN = 4614.0
HIDDEN_ERPM_OFFSET = 0.0
HIDDEN_SERVO_GAIN = -1.2135
HIDDEN_SERVO_OFFSET = 0.5304
WHEELBASE = 0.3302

class SimOdomCalibrator(Node):
    def __init__(self):
        super().__init__('sim_odom_calibrator')
        self.declare_parameter('speed_to_erpm_gain', 4000.0)
        self.declare_parameter('speed_to_erpm_offset', 0.0)
        self.declare_parameter('steering_angle_to_servo_gain', -1.0)
        self.declare_parameter('steering_angle_to_servo_offset', 0.5)

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.last_erpm = 0.0
        self.last_servo = HIDDEN_SERVO_OFFSET

        self.create_subscription(
            AckermannDriveStamped, '/drive', self.drive_callback, 10)
        self.odom_pub = self.create_publisher(Odometry, '/odom_estimated', 10)
        self.tf_broadcaster = TransformBroadcaster(self)
        self.last_time = self.get_clock().now()
        self.create_timer(0.02, self.integrate)

    def drive_callback(self, msg):
        cmd_speed = msg.drive.speed
        cmd_steer = msg.drive.steering_angle
        self.last_erpm = cmd_speed * HIDDEN_ERPM_GAIN + HIDDEN_ERPM_OFFSET
        self.last_servo = cmd_steer * HIDDEN_SERVO_GAIN + HIDDEN_SERVO_OFFSET

    def integrate(self):
        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds / 1e9
        self.last_time = now

        gain = self.get_parameter('speed_to_erpm_gain').value
        offset = self.get_parameter('speed_to_erpm_offset').value
        servo_gain = self.get_parameter('steering_angle_to_servo_gain').value
        servo_offset = self.get_parameter('steering_angle_to_servo_offset').value

        est_speed = (self.last_erpm - offset) / gain
        est_steer = (self.last_servo - servo_offset) / servo_gain

        self.x += est_speed * math.cos(self.theta) * dt
        self.y += est_speed * math.sin(self.theta) * dt
        self.theta += est_speed * math.tan(est_steer) / WHEELBASE * dt

        self.publish_odom(now, est_speed)

    def publish_odom(self, now, est_speed):
        q = Quaternion(z=math.sin(self.theta / 2.0), w=math.cos(self.theta / 2.0))

        odom = Odometry()
        odom.header.stamp = now.to_msg()
        odom.header.frame_id = 'odom_estimated'
        odom.child_frame_id = 'base_link_estimated'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation = q
        odom.twist.twist.linear.x = est_speed
        self.odom_pub.publish(odom)

        t = TransformStamped()
        t.header.stamp = now.to_msg()
        t.header.frame_id = 'odom_estimated'
        t.child_frame_id = 'base_link_estimated'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.rotation = q
        self.tf_broadcaster.sendTransform(t)

def main():
    rclpy.init()
    rclpy.spin(SimOdomCalibrator())

if __name__ == '__main__':
    main()
