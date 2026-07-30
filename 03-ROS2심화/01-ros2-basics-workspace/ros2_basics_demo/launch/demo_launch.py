"""3장 실습 — 다섯 노드를 파라미터·리매핑과 함께 한 번에 실행하는 launch 파일."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2_basics_demo',
            executable='heartbeat_publisher',
            name='heartbeat_publisher',
            parameters=[{'publish_rate_hz': 2.0}],
        ),
        Node(
            package='ros2_basics_demo',
            executable='heartbeat_subscriber',
            name='heartbeat_subscriber',
            remappings=[('heartbeat', 'car/heartbeat')],
        ),
        Node(
            package='ros2_basics_demo',
            executable='mode_service_server',
            name='mode_service_server',
        ),
        Node(
            package='ros2_basics_demo',
            executable='laser_tf_broadcaster',
            name='laser_tf_broadcaster',
        ),
        Node(
            package='ros2_basics_demo',
            executable='laser_tf_listener',
            name='laser_tf_listener',
        ),
    ])
