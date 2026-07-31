# 나만의 ROS2 패키지 + launch 파일 만들기

책 본문 3.7절과 짝을 이루는 실습입니다. 패키지 두 개(인터페이스 + 노드)로 Pub/Sub, 서비스, TF를
모두 갖춘 미니 프로젝트를 완성합니다.

## 구성

```
ros2_basics_interfaces/       (ament_cmake) — 커스텀 서비스 정의
  srv/SetDriveMode.srv
ros2_basics_demo/             (ament_python) — 실제 동작하는 노드들
  ros2_basics_demo/
    heartbeat_publisher.py    — /heartbeat(std_msgs/String) 발행 (Pub)
    heartbeat_subscriber.py   — /heartbeat 구독, 로그 출력 (Sub)
    mode_service_server.py    — /set_drive_mode 서비스 서버 (Server)
    laser_tf_broadcaster.py   — base_link -> laser 정적 TF 발행
    laser_tf_listener.py      — base_link -> laser TF 조회
  launch/
    demo_launch.py            — 위 다섯 노드를 파라미터·리매핑과 함께 한 번에 실행
```

## 설치

이 폴더 안의 `ros2_basics_interfaces/`와 `ros2_basics_demo/` 두 폴더를 그대로
`~/ros2_ws/src/` 아래로 복사(또는 심볼릭 링크)합니다.

```bash
cp -r ros2_basics_interfaces ros2_basics_demo ~/ros2_ws/src/
cd ~/ros2_ws
source /opt/ros/humble/setup.bash   # 사용 중인 배포판에 맞게
colcon build --packages-select ros2_basics_interfaces ros2_basics_demo
source install/setup.bash
```

## 실행

```bash
ros2 launch ros2_basics_demo demo_launch.py
```

새 터미널에서 (매번 `source install/setup.bash` 먼저):

```bash
ros2 topic echo /car/heartbeat
ros2 service call /set_drive_mode ros2_basics_interfaces/srv/SetDriveMode "{mode: 'auto'}"
ros2 run tf2_ros tf2_echo base_link laser
```

`tf2_echo`가 `Translation: [0.275, 0.0, 0.0]` 근처 값을 출력하면 성공입니다.
`ros2 run tf2_tools view_frames`로 좌표계 트리를 PDF로도 확인할 수 있습니다.

## 왜 패키지가 두 개인가

커스텀 `.srv`/`.msg`/`.action`은 `rosidl` 코드 생성 도구가 CMake 빌드 단계에서 파이썬·C++ 양쪽
코드를 만들어내기 때문에, 파이썬 노드 코드(`ament_python`)와 같은 패키지에 둘 수 없습니다. 그래서
인터페이스 정의(`ros2_basics_interfaces`, `ament_cmake`)와 노드 코드(`ros2_basics_demo`,
`ament_python`)를 분리했습니다. 자세한 설명은 책 본문 3.2절을 참고하세요.
