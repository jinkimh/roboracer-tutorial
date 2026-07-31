#!/usr/bin/env python3
"""3.3절 — TF 최소 예제(정적 브로드캐스터).

base_link -> laser 정적 변환을 발행한다. 패키지 없이 python3로 바로
실행할 수 있다. 3.7절 실습(laser_tf_broadcaster.py)의 축소판이다.
"""

import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped


class MinimalTFBroadcaster(Node):
    def __init__(self):
        super().__init__('minimal_tf_broadcaster')
        self.broadcaster = StaticTransformBroadcaster(self)
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'laser'
        t.transform.translation.x = 0.275
        t.transform.rotation.w = 1.0  # 회전 없음
        self.broadcaster.sendTransform(t)
        self.get_logger().info('base_link -> laser 정적 TF 발행 (x=0.275m)')


def main(args=None):
    rclpy.init(args=args)
    node = MinimalTFBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
