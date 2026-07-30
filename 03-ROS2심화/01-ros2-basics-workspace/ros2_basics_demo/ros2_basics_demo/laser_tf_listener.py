#!/usr/bin/env python3
"""3장 실습 — base_link -> laser TF를 주기적으로 조회해 출력하는 리스너."""

import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class LaserTFListener(Node):
    def __init__(self):
        super().__init__('laser_tf_listener')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(2.0, self.lookup_transform)

    def lookup_transform(self):
        try:
            t = self.tf_buffer.lookup_transform('base_link', 'laser', rclpy.time.Time())
            self.get_logger().info(
                f'base_link -> laser: x={t.transform.translation.x:.3f}m'
            )
        except TransformException as ex:
            self.get_logger().warn(f'TF 조회 실패: {ex}')


def main(args=None):
    rclpy.init(args=args)
    node = LaserTFListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
