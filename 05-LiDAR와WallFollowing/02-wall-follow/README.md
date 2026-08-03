# Wall Following — wall_follow_node

책 본문 [5.5절](../../../manuscript/05-LiDAR와WallFollowing/05-LiDAR와WallFollowing.md#55-🖥️-실습--wall-following-알고리즘-실행-시뮬레이터)(시뮬레이터)·
[5.7절](../../../manuscript/05-LiDAR와WallFollowing/05-LiDAR와WallFollowing.md#57-🚗-실습--실차-버전-코드-수정-없이-실행하기)(실차)과 짝을 이루는 실습입니다.
패키지 없이 `python3 wall_follow_node.py`로 바로 실행할 수 있고, **시뮬레이터·실차 어느 쪽에서도 코드
수정 없이 동일하게 동작**합니다.

LiDAR 두 빔(옆면 90°, 진행방향 쪽 90°−θ)으로 벽까지의 거리·접근각을 계산하고, PID 제어로 목표 거리를
유지하며 조향각을 결정합니다.

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
