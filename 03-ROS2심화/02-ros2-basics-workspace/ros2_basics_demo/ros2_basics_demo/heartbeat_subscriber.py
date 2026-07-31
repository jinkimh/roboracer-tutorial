#!/usr/bin/env python3
"""3장 실습 — /heartbeat 토픽을 구독해 받은 메시지를 로그로 출력하는 서브스크라이버.

launch/demo_launch.py에서 'heartbeat' -> 'car/heartbeat'로 리매핑되어 실행된다.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HeartbeatSubscriber(Node):
    def __init__(self):
        super().__init__('heartbeat_subscriber')
        self.subscription = self.create_subscription(
            String, 'heartbeat', self.listener_callback, 10)

    def listener_callback(self, msg: String):
        self.get_logger().info(f'받음: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = HeartbeatSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
