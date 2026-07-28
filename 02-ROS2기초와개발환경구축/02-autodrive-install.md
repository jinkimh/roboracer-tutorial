# AutoDRIVE 시뮬레이터 설치와 첫 실행

책 본문 2.6절과 짝을 이루는 실습입니다. 개념 설명은 본문을 참고하고, 여기서는 명령어만 간결하게 정리합니다.
별도로 저장할 코드 파일이 없어 이 문서 하나로 관리합니다.

## 사전 준비

- 호스트에 ROS2가 설치되어 있어야 합니다(Ubuntu 22.04 기준 ROS2 Humble 권장). 미설치 시 [공식 설치 가이드](https://docs.ros.org/en/humble/Installation.html) 참고.

## Step 1. AutoDRIVE Simulator 내려받기

[AutoDRIVE 릴리스 페이지](https://github.com/Tinker-Twins/AutoDRIVE/releases)에서 최신 Simulator를 OS에 맞게 내려받습니다. 압축을 풀고 바로 실행할 수 있는 독립 실행형 앱입니다.

## Step 2. ROS2 API(Devkit) 설치

```bash
mkdir -p ~/autodrive_ws/src
git clone --single-branch --branch AutoDRIVE-Devkit https://github.com/Tinker-Twins/AutoDRIVE.git ~/AutoDRIVE-Devkit
mv ~/AutoDRIVE-Devkit/"ADSS Toolkit"/autodrive_ros2 ~/autodrive_ws/src/
```

```bash
pip3 install eventlet==0.33.3 Flask==1.1.1 Flask-SocketIO==4.1.0 \
  python-socketio==4.2.0 python-engineio==3.13.0 greenlet==1.0.0 \
  gevent==21.1.2 gevent-websocket==0.10.1 Jinja2==3.0.3 \
  itsdangerous==2.0.1 werkzeug==2.0.3
pip3 install attrdict numpy pillow opencv-contrib-python
```

```bash
cd ~/autodrive_ws
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

## Step 3. 실행

1. Step 1에서 받은 AutoDRIVE Simulator 앱을 실행하고, 시작 화면에서 F1TENTH 차량과 트랙 환경을 선택합니다.
2. 시뮬레이터를 켠 상태에서 ROS2 브리지를 켭니다.

```bash
source ~/autodrive_ws/install/setup.bash
ros2 launch autodrive_f1tenth simulator_bringup_rviz.launch.py
# 가벼운 실행이 필요하면: simulator_bringup_headless.launch.py
```

## 텔레옵

```bash
ros2 run autodrive_f1tenth teleop_keyboard
```

`w`/`s`(가속/감속) `a`/`d`(좌/우 조향) `q`(조향 중앙 복귀) `e`(비상 정지) `x`(강제 정지 및 초기화)

## 문제 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| `colcon build`에서 `rclpy`/`std_msgs` 못 찾음 | ROS2 미source | `source /opt/ros/humble/setup.bash` 먼저 실행 |
| 브리지 실행해도 시뮬레이터 무반응 | 시뮬레이터 앱 미실행 또는 포트 충돌 | 시뮬레이터 앱을 먼저 켜고 브리지 실행 |
| `pip3 install` 버전 충돌 | 시스템 파이썬과 충돌 | `venv` 가상환경 안에서 설치 |
