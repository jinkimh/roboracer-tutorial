#!/usr/bin/env python3
"""3.1절 — Pub/Sub 최소 예제(발행자).

패키지 없이 python3 minimal_publisher.py로 바로 실행할 수 있다(2장의
my_first_listener_node.py와 같은 방식).
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'greeting', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'안녕, ROS2! ({self.i})'
        self.publisher_.publish(msg)
        self.get_logger().info(f'발행: {msg.data}')
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
