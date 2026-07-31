#!/usr/bin/env python3
"""3.1절 — Action 최소 예제(서버).

example_interfaces/action/Fibonacci도 ROS2 기본 설치에 포함되어 있다.
Fibonacci.action 정의는 3.2절 참고.

실행: python3 fibonacci_action_server.py
클라이언트(다른 터미널): ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 5}" --feedback
"""

import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self, Fibonacci, 'fibonacci', self.execute_callback)
        self.get_logger().info('fibonacci 액션 서버 시작')

    def execute_callback(self, goal_handle):
        sequence = [0, 1]
        feedback_msg = Fibonacci.Feedback()

        for i in range(1, goal_handle.request.order):
            sequence.append(sequence[i] + sequence[i - 1])
            feedback_msg.partial_sequence = sequence
            self.get_logger().info(f'진행 중: {sequence}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)  # 실제로 시간이 걸리는 작업을 흉내

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = sequence
        return result


def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
