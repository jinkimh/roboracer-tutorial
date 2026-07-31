#!/usr/bin/env python3
"""3.1절 — Action 최소 예제(클라이언트). fibonacci_action_server.py와 짝을 이룬다.

실행: python3 fibonacci_action_client.py <order>
예: python3 fibonacci_action_client.py 5
"""

import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('목표가 거부되었습니다')
            return
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'최종 결과: {result.sequence}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'진행 중: {feedback.partial_sequence}')


def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionClient()
    node.send_goal(int(sys.argv[1]))
    rclpy.spin(node)


if __name__ == '__main__':
    main()
