#!/usr/bin/env python3
"""2.7절 "LLM과 함께 구현하기"의 참고 답안 노드.

ROS2 패키지를 새로 만들지 않고, ROS2 환경을 source한 터미널에서
    python3 my_first_listener_node.py
로 바로 실행할 수 있는 "첫 ROS2 노드" 예시입니다.

F1TENTH Gym 시뮬레이터가 /drive 토픽으로 내보내는
AckermannDriveStamped 메시지를 구독해, 속도와 조향각을 사람이
읽기 좋은 형태로 출력합니다.

AutoDRIVE 시뮬레이터로 실습 중이라면 아래 "구독 대상 바꾸기" 안내를
따라 토픽 이름/메시지 타입만 바꿔주면 동일한 코드 구조로 동작합니다.
"""

import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped


class MyFirstListener(Node):
    def __init__(self):
        super().__init__('my_first_listener')
        self.subscription = self.create_subscription(
            AckermannDriveStamped,
            'drive',
            self.listener_callback,
            10,
        )
        self.get_logger().info('my_first_listener 노드 시작 — /drive 토픽 구독 중')

    def listener_callback(self, msg: AckermannDriveStamped):
        speed = msg.drive.speed
        steering_angle = msg.drive.steering_angle
        self.get_logger().info(
            f'속도={speed:.2f} m/s, 조향각={steering_angle:.2f} rad'
        )


def main(args=None):
    rclpy.init(args=args)
    node = MyFirstListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

# --- 구독 대상 바꾸기 (AutoDRIVE 시뮬레이터용) ---
# AutoDRIVE는 조향/스로틀을 서로 다른 토픽, 서로 다른 메시지 타입으로 내보냅니다.
#   from std_msgs.msg import Float32
#   self.sub_throttle = self.create_subscription(
#       Float32, '/autodrive/f1tenth_1/throttle_command', self.throttle_callback, 10)
#   self.sub_steering = self.create_subscription(
#       Float32, '/autodrive/f1tenth_1/steering_command', self.steering_callback, 10)
# 정확한 토픽 이름과 타입은 실습 중인 시뮬레이터에서
# `ros2 topic list`와 `ros2 topic info <토픽이름>`으로 항상 직접 확인하세요.
