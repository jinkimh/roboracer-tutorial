# Wall Following — wall_follow_node

책 본문 [5.5절](../../../manuscript/05-LiDAR와WallFollowing/05-LiDAR와WallFollowing.md#55-🖥️-실습--wall-following-알고리즘-실행-시뮬레이터)(시뮬레이터)·
[5.7절](../../../manuscript/05-LiDAR와WallFollowing/05-LiDAR와WallFollowing.md#57-🚗-실습--실차-버전-코드-수정-없이-실행하기)(실차)과 짝을 이루는 실습입니다.
패키지 없이 `python3 wall_follow_node.py`로 바로 실행할 수 있고, **시뮬레이터·실차 어느 쪽에서도 코드
수정 없이 동일하게 동작**합니다.

LiDAR 두 빔(옆면 90°, 진행방향 쪽 90°−θ)으로 벽까지의 거리·접근각을 계산하고, PID 제어로 목표 거리를
유지하며 조향각을 결정합니다.

토픽(`/scan`, `/drive`)·메시지 타입·알고리즘은 [jinkimh/f1tenth-software-stack의 `wall_follow`
패키지](https://github.com/jinkimh/f1tenth-software-stack/tree/main/wall_follow)(원저작:
University of Pennsylvania F1TENTH 팀)와 그대로 맞춰뒀습니다 — 실제 레이스에 쓰인 코드와 같은
방식으로 통신하므로, 이 노드는 실제 드라이버 스택·시뮬레이터 어느 쪽에도 수정 없이 꽂아 쓸 수
있습니다. 다만 두 가지는 의도적으로 다르게(더 견고하게) 만들었습니다.

- **배열 인덱스 계산**: 원본은 LiDAR 사양(−135°, 0.25°/빔)에 맞춘 계산식을 하드코딩했지만, 이 노드는
  `scan.angle_min`/`scan.angle_increment`로 매번 계산합니다 — 다른 LiDAR·다른 설정에서도 안전합니다.
- **Δt 계산**: `scan.header.stamp`(센서 타임스탬프) 기준으로 계산해, ROS2 메시지 전달 지연이 미분
  항에 섞이지 않게 했습니다.

원본에 있던 "전방 빔이 가까우면 강제로 감속·조향"하는 임시 안전 로직은 넣지 않았습니다 — 그 역할은
6장(Emergency Braking)에서 별도 노드로 제대로 다룹니다.

## 실행

```bash
source /opt/ros/humble/setup.bash   # 사용 중인 배포판에 맞게
python3 wall_follow_node.py
```

기본값은 왼쪽 벽(`side=left`)을 목표 거리 1.0m로 따라갑니다.

## 파라미터

| 이름 | 기본값 | 의미 |
|---|---|---|
| `side` | `left` | 따라갈 벽(`left` 또는 `right`) |
| `desired_distance` | `1.0` | 목표 거리(m) |
| `lookahead` | `1.0` | 예상 거리 계산에 쓰는 lookahead 거리 L(m) |
| `theta_deg` | `50.0` | 두 빔 사이 각도 θ(도) |
| `kp`, `ki`, `kd` | `1.0`, `0.0`, `0.05` | PID 게인 |
| `max_speed` | `1.5` | 최대 속도(m/s) — 실차에서는 낮춰서 시작 |

```bash
ros2 param set /wall_follow_node kd 0.15
ros2 param set /wall_follow_node side right
```

## 실차에서

4.7절 드라이버 스택을 먼저 브링업한 뒤, 같은 명령으로 실행하되 **속도를 낮춰서 시작**하세요.

```bash
python3 wall_follow_node.py --ros-args -p max_speed:=0.8
```

코드는 동일합니다 — 무엇이, 왜 그대로 동작하는지는 본문 5.7절을 참고하세요.
