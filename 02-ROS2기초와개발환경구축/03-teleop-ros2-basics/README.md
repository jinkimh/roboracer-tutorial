# 텔레옵으로 ROS2 손에 익히기 + 첫 ROS2 노드 만들기

책 본문 2.7절과 짝을 이루는 실습입니다.

## ROS2 명령어로 관찰하기

시뮬레이터(F1TENTH Gym 또는 AutoDRIVE)와 텔레옵을 켠 상태에서 새 터미널을 열고 ROS2 환경을 source한 뒤:

```bash
ros2 node list      # 지금 실행 중인 노드 목록
ros2 topic list     # 지금 오가는 토픽 목록
ros2 topic echo /drive        # F1TENTH Gym: 텔레옵이 실제로 보내는 값 확인
ros2 topic info /drive        # 메시지 타입, 발행자/구독자 수
```

AutoDRIVE라면 `/drive` 대신 `/autodrive/f1tenth_1/throttle_command`, `/autodrive/f1tenth_1/steering_command`를 사용합니다.

| 시뮬레이터 | 토픽 이름 | 메시지 타입 |
|---|---|---|
| F1TENTH Gym | `/drive` | `ackermann_msgs/AckermannDriveStamped` (speed, steering_angle) |
| AutoDRIVE | `/autodrive/f1tenth_1/throttle_command`, `/autodrive/f1tenth_1/steering_command` | `std_msgs/Float32` (-1.0~1.0) |

## 🤖 LLM과 함께 나만의 첫 ROS2 노드 만들기

ROS2 패키지를 새로 만들지 않고, ROS2 환경이 source된 터미널에서 `python3 my_first_listener_node.py`로
바로 실행할 수 있는 노드를 LLM에게 요청합니다.

> **프롬프트 템플릿**
>
> "ROS2(rclpy)를 사용하는 파이썬 노드를 하나 작성해줘. 조건은 다음과 같아:
> 1. 토픽 이름 `/drive`, 메시지 타입 `ackermann_msgs.msg.AckermannDriveStamped`를 구독하는 노드야.
> 2. 메시지를 받을 때마다 `speed`와 `steering_angle` 값을 사람이 읽기 쉬운 형태로 출력해줘.
> 3. `ros2 pkg create` 같은 패키지 생성 없이, `python3 파일이름.py`로 바로 실행할 수 있는 단일 파일 스크립트로 작성해줘.
> 4. `rclpy.init()`, `rclpy.spin()`, `rclpy.shutdown()`을 정확한 순서로 포함해줘."

### 검증 체크리스트

- [ ] `import rclpy`, `from rclpy.node import Node`가 있는가
- [ ] 구독 토픽 이름이 `ros2 topic list` 결과와 정확히 일치하는가(맨 앞 `/` 포함)
- [ ] 메시지 타입 import가 되는가 — `python3 -c "from ackermann_msgs.msg import AckermannDriveStamped"`로 먼저 확인
- [ ] `rclpy.spin(node)`가 있는가 — 없으면 메시지를 못 받고 바로 종료됨
- [ ] 콜백 함수가 메시지 하나를 인자로 받는가(`def callback(self, msg):`)

### 실행

```bash
python3 my_first_listener_node.py
```

[`my_first_listener_node.py`](my_first_listener_node.py)에 참고 답안이 있습니다. AutoDRIVE로 실습 중이라면
파일 안의 "구독 대상 바꾸기" 안내를 따라 토픽 이름과 메시지 타입만 바꿔주면 동일하게 동작합니다.
