from setuptools import find_packages, setup

package_name = 'key_teleop'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jin Kim',
    maintainer_email='jin.kim@gnu.ac.kr',
    description='4장 실습 — 키보드 입력을 AckermannDriveStamped로 변환하는 실차 텔레옵 노드',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'commander_node = key_teleop.commander_node:main',
        ],
    },
)
