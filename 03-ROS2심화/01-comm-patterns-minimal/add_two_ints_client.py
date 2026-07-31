#!/usr/bin/env python3
"""3.1절 — Server/Client 최소 예제(클라이언트). add_two_ints_server.py와 짝을 이룬다.

실행: python3 add_two_ints_client.py <a> <b>
예: python3 add_two_ints_client.py 3 5
"""

import sys

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('서비스를 기다리는 중...')

    def send_request(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        return future.result()


def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClient()
    a, b = int(sys.argv[1]), int(sys.argv[2])
    response = node.send_request(a, b)
    node.get_logger().info(f'결과: {a} + {b} = {response.sum}')
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
