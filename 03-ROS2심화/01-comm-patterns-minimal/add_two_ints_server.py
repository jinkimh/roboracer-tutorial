#!/usr/bin/env python3
"""3.1절 — Server/Client 최소 예제(서버).

example_interfaces는 ROS2 기본 설치에 포함된 표준 인터페이스 패키지라
별도로 만들 필요가 없다. 커스텀 서비스를 만드는 법은 3.2절에서 다룬다.

실행: python3 add_two_ints_server.py
클라이언트(다른 터미널): ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 3, b: 5}"
"""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddTwoIntsServer(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.handle_request)
        self.get_logger().info('add_two_ints 서비스 서버 시작')

    def handle_request(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'{request.a} + {request.b} = {response.sum}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
