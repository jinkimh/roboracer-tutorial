#!/usr/bin/env python3
"""3.1절 — Pub/Sub 최소 예제(구독자). minimal_publisher.py와 짝을 이룬다."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String, 'greeting', self.listener_callback, 10)

    def listener_callback(self, msg: String):
        self.get_logger().info(f'받음: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
