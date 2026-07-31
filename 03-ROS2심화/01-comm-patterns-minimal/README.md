# 통신 패턴 최소 예제 — Pub/Sub, Server/Client, Action

책 본문 3.1절과 짝을 이루는 실습입니다. 패키지를 만들지 않고, ROS2 환경을 source한 터미널에서
`python3 파일이름.py`로 바로 실행할 수 있는 최소 예제들입니다(2장의 `my_first_listener_node.py`와
같은 방식). 커스텀 서비스를 직접 만드는 법은 [02-ros2-basics-workspace](../02-ros2-basics-workspace/)에서 다룹니다.

## Pub/Sub

```bash
source /opt/ros/humble/setup.bash   # 사용 중인 배포판에 맞게
python3 minimal_publisher.py
```

새 터미널에서:

```bash
source /opt/ros/humble/setup.bash
python3 minimal_subscriber.py
# 또는
ros2 topic echo /greeting
```

## Server/Client

```bash
source /opt/ros/humble/setup.bash
python3 add_two_ints_server.py
```

새 터미널에서(클라이언트 역할):

```bash
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 3, b: 5}"
```

## Action

```bash
source /opt/ros/humble/setup.bash
python3 fibonacci_action_server.py
```

새 터미널에서(클라이언트 역할):

```bash
ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 5}" --feedback
```

`--feedback`을 주면 계산이 끝날 때까지 중간 진행 상황이 1초 간격으로 출력됩니다 — 서비스라면
볼 수 없는 부분입니다.

## 참고

`example_interfaces`는 ROS2 기본 설치에 포함된 표준 인터페이스 패키지라 별도로 만들 필요가
없습니다. 여러분만의 서비스/메시지를 정의하는 법(`.srv`, `.msg`)은 책 본문 3.2절과
[02-ros2-basics-workspace](../02-ros2-basics-workspace/)를 참고하세요.
