# 실차 키보드 텔레옵 — key_teleop

책 본문 [4.7절](../../../manuscript/04-차량모델링과좌표계/04-차량모델링과좌표계.md#step-0-첫-브링업--키보드로-움직여보기) Step 0과 짝을 이루는 실습입니다.
원본 부트캠프 자료(`Lab-04-F1Tenth_control_by_keyboard_Ko.md`)의 키보드 텔레옵을 ROS2 Humble·이 책의
파라미터 선언 스타일(3.5절)에 맞춰 재구성했습니다.

`ros2-keyboard`[8]가 발행하는 `/keydown`(keyboard_msgs/Key)을 구독해, 방향키·스페이스바를
`AckermannDriveStamped`(`/drive`)로 변환합니다. 실차·시뮬레이터 어느 쪽에서도 동일하게 동작합니다.

## 사전 준비 — ros2-keyboard 설치

```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone https://github.com/cmower/ros2-keyboard.git
sudo apt install -y libsdl1.2-dev
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select keyboard
```

## 이 패키지(key_teleop) 빌드

이 폴더(`key_teleop/`)를 `~/ros2_ws/src/`에 복사한 뒤:

```bash
cd ~/ros2_ws
colcon build --packages-select key_teleop
source install/setup.bash
```

## 실행

```bash
# 터미널 A
ros2 run keyboard keyboard --ros-args -p allow_repeat:=true
# 터미널 B
ros2 run key_teleop commander_node
```

입력창을 클릭한 뒤 방향키(↑↓←→)와 스페이스바로 `/drive`에 명령이 발행되는지 `ros2 topic echo /drive`로
확인하세요. 속도·조향각은 `speed_forward`, `speed_reverse`, `steer_angle_deg` 파라미터로 조정할 수
있습니다.

```bash
ros2 run key_teleop commander_node --ros-args -p speed_forward:=1.5
```
