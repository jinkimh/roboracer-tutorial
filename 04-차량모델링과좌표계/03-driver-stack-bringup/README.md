# 실차 드라이버 스택 브링업 — f1tenth_system + sensors.yaml

책 본문 [4.7절](../../../manuscript/04-차량모델링과좌표계/04-차량모델링과좌표계.md#step-1-드라이버-스택-워크스페이스-구성) Step 1~2와 짝을 이루는 실습 자료입니다.
VESC·LiDAR·조이스틱 드라이버를 한데 묶은 `f1tenth_system`[5] 워크스페이스를 구성하고,
LiDAR를 설정해 첫 bringup을 실행합니다.

## Step 1. 워크스페이스 구성

```bash
mkdir -p ~/f1tenth_ws/src && cd ~/f1tenth_ws
colcon build   # 빈 워크스페이스 초기화
cd src
git clone https://github.com/f1tenth/f1tenth_system.git
cd f1tenth_system
git submodule update --init --force --remote
cd ~/f1tenth_ws
rosdep update
rosdep install --from-paths src -i -y
colcon build
```

## Step 2. LiDAR 설정

이 폴더의 **[sensors.yaml](sensors.yaml)**을 `f1tenth_ws/src/f1tenth_system/f1tenth_stack/config/sensors.yaml`에
덮어쓰고, 차량에 달린 LiDAR 종류(이더넷/USB)에 맞는 쪽만 남기세요.

> 💡 **USB LiDAR를 쓴다면**: `/dev/ttyUSB0` 같은 이름은 USB 포트를 꽂은 순서·재부팅에 따라 바뀔 수
> 있습니다. `udevadm info -a -n /dev/ttyUSB0`로 시리얼 번호를 확인해 `/etc/udev/rules.d/`에 고정
> 이름(예: `/dev/ttyUSB_LIDAR`)을 매핑하는 udev 규칙을 만들어두면, 케이블을 뽑았다 꽂아도 `sensors.yaml`을
> 다시 고칠 필요가 없습니다.

## Bringup 실행

```bash
source /opt/ros/humble/setup.bash
cd ~/f1tenth_ws
source install/setup.bash
ros2 launch f1tenth_stack bringup_launch.py
```

VESC·LiDAR·조이스틱 드라이버가 한 번에 켜집니다. 새 터미널에서 `rviz2`를 실행하고 `LaserScan`
디스플레이를 `/scan` 토픽으로 추가해 라이다 스캔이 보이는지 확인하세요.

이후 [02-real-keyboard-teleop](../02-real-keyboard-teleop/)의 텔레옵 노드로 첫 주행을(4.7절 Step 3),
[04-real-odom-tuning](../04-real-odom-tuning/)으로 오도메트리 튜닝을(4.7절 Step 4) 진행합니다.
