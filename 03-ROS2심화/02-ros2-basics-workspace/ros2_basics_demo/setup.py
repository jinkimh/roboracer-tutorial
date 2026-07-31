import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'ros2_basics_demo'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*_launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jin Kim',
    maintainer_email='jin.kim@gnu.ac.kr',
    description='3장 실습 — Pub/Sub, 서비스, TF를 갖춘 미니 ROS2 프로젝트',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'heartbeat_publisher = ros2_basics_demo.heartbeat_publisher:main',
            'heartbeat_subscriber = ros2_basics_demo.heartbeat_subscriber:main',
            'mode_service_server = ros2_basics_demo.mode_service_server:main',
            'laser_tf_broadcaster = ros2_basics_demo.laser_tf_broadcaster:main',
            'laser_tf_listener = ros2_basics_demo.laser_tf_listener:main',
        ],
    },
)
