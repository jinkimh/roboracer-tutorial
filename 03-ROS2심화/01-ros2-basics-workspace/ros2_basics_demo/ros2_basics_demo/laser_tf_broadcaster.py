#!/usr/bin/env python3
"""3장 실습 — base_link -> laser 정적 TF를 발행하는 브로드캐스터.

라이다는 차체에 고정되어 있어 시간이 지나도 관계가 바뀌지 않으므로
(동적 TransformBroadcaster가 아니라) StaticTransformBroadcaster를 쓴다.
x=0.275m는 F1TENTH Gym 시뮬레이터의 scan_distance_to_base_link와 같은 값이다.
"""

import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped


class LaserTFBroadcaster(Node):
    def __init__(self):
        super().__init__('laser_tf_broadcaster')
        self.broadcaster = StaticTransformBroadcaster(self)
        self.broadcast_transform()

    def broadcast_transform(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'laser'
        t.transform.translation.x = 0.275
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0
        self.broadcaster.sendTransform(t)
        self.get_logger().info('base_link -> laser 정적 TF 발행 (x=0.275m)')


def main(args=None):
    rclpy.init(args=args)
    node = LaserTFBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
