#!/usr/bin/env python3
"""3장 실습 — /heartbeat 토픽에 주기적으로 문자열을 발행하는 퍼블리셔.

publish_rate_hz 파라미터로 발행 주기를 바꿀 수 있다 (launch/demo_launch.py에서 2.0으로 지정).
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HeartbeatPublisher(Node):
    def __init__(self):
        super().__init__('heartbeat_publisher')
        self.declare_parameter('publish_rate_hz', 1.0)
        rate_hz = self.get_parameter('publish_rate_hz').value
        self.publisher_ = self.create_publisher(String, 'heartbeat', 10)
        self.timer = self.create_timer(1.0 / rate_hz, self.timer_callback)
        self.count = 0
        self.get_logger().info(f'heartbeat_publisher 시작 — {rate_hz} Hz로 발행')

    def timer_callback(self):
        msg = String()
        msg.data = f'heartbeat #{self.count}'
        self.publisher_.publish(msg)
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = HeartbeatPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
