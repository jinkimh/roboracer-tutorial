#!/usr/bin/env python3
"""3장 실습 — /set_drive_mode 서비스 서버.

ros2_basics_interfaces/srv/SetDriveMode를 사용한다. 클라이언트 코드는 따로 작성하지 않고
`ros2 service call`을 클라이언트로 쓴다.
"""

import rclpy
from rclpy.node import Node
from ros2_basics_interfaces.srv import SetDriveMode


class ModeServiceServer(Node):
    def __init__(self):
        super().__init__('mode_service_server')
        self.current_mode = 'manual'
        self.srv = self.create_service(
            SetDriveMode, 'set_drive_mode', self.handle_request)
        self.get_logger().info('mode_service_server 시작 — 현재 모드: manual')

    def handle_request(self, request, response):
        if request.mode not in ('manual', 'auto'):
            response.success = False
            response.message = f'알 수 없는 모드입니다: {request.mode}'
            return response
        self.current_mode = request.mode
        response.success = True
        response.message = f'모드를 {request.mode}로 변경했습니다'
        self.get_logger().info(response.message)
        return response


def main(args=None):
    rclpy.init(args=args)
    node = ModeServiceServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
