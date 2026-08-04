# 안전 계층 — simple_safety_node

책 본문 [6.4절](../../../manuscript/06-안전계층EmergencyBraking/06-안전계층EmergencyBraking.md#64-🖥️-실습--simple-safety-node-구현)(시뮬레이터)·
[6.6절](../../../manuscript/06-안전계층EmergencyBraking/06-안전계층EmergencyBraking.md#66-🚗-실습--실차-버전-실차-안전-수칙과-검증-절차)(실차)과 짝을 이루는 실습입니다.
패키지 없이 `python3 simple_safety_node.py`로 바로 실행할 수 있습니다.

LiDAR 정면 부채꼴(기본 ±10°)의 거리와 차량 자신의 속도로 Time-to-Collision(TTC)을 계산해,
임계값 아래로 떨어지면 속도를 0으로 만들고 다시 복구하지 않는 자동 긴급제동(AEB) 노드입니다.
이 노드는 다른 주행 로직(Wall Following 등)과 결합하지 않는 **단독 실행 데모**입니다 —
`steering_angle`은 항상 0(직진)이고 `speed`만 관리합니다. 단독으로 실행해 벽 앞에서 실제로
멈추는지만 검증하는 것이 이 실습의 목표입니다(왜 이렇게 설계했는지는 본문 6.3절 참고).

원본 알고리즘(TTC 임계값 0.8초, 전진/후진 임계값 비대칭)은 [jinkimh/f1tenth-software-stack의
`simple_safety_node`](https://github.com/jinkimh/f1tenth-software-stack/blob/main/simple_safety_node/simple_safety_node/simple_safety_node.py)를
따르되, 실제로 검증해보니 있던 두 가지 결함을 고쳤습니다(본문 6.3절에서 자세히 다룹니다).

- **배열 인덱스 계산**: 원본은 이 책의 표준 LiDAR 사양에 맞춘 계산식(`539 + int(angle*4)`)을
  하드코딩했지만, 이 노드는 `scan.angle_min`/`scan.angle_increment`로 매번 계산합니다.
- **각도 단위(도→라디안) 변환**: 원본은 도(degree) 값을 변환 없이 그대로 `np.cos()`에 넣는 실제
  버그가 있습니다 — 정면(0°)에서는 우연히 값이 맞지만, 부채꼴 가장자리(±10°)에서는 `cos(10
  라디안)` ≈ −0.84가 계산되어 TTC가 60초로 튀어버려 장애물을 놓칩니다. 이 노드는
  `math.radians()`로 변환한 뒤 `cos()`에 넣어 이 결함을 고쳤습니다.

## 실행

```bash
source /opt/ros/humble/setup.bash   # 사용 중인 배포판에 맞게
python3 simple_safety_node.py
```

시뮬레이터에서 차량을 벽을 정면으로 바라보는 위치에 두고 실행하면, 기본 속도(2.0 m/s)로 직진을
시작해 정면 벽까지 거리가 약 1.6m 아래로 떨어지는 순간 멈춥니다.

## 파라미터

| 이름 | 기본값 | 의미 |
|---|---|---|
| `odom_topic` | `/ego_racecar/odom` | 오도메트리 토픽(시뮬레이터 기본값) — 실차에서는 `/odom`으로 전환 |
| `desired_speed` | `2.0` | 위험이 감지되기 전까지 유지하는 목표 속도(m/s) |
| `fov_deg` | `10.0` | 정면 기준 좌우 스캔 범위(도) |
| `ttc_threshold` | `0.8` | 전진 중 정지를 트리거하는 TTC 임계값(초) |
| `reverse_ttc_offset` | `0.8` | 후진 중 임계값에 더하는 오프셋(후진 임계값 = `ttc_threshold + reverse_ttc_offset`) |

```bash
ros2 param set /simple_safety_node ttc_threshold 0.4
ros2 param set /simple_safety_node fov_deg 20.0
```

## 실차에서

4.7절 드라이버 스택을 먼저 브링업한 뒤, **정비 스탠드 위 → 저속 주행 → 실제 주행** 순서로
검증하세요. 조이스틱(비상 정지)을 항상 손에 쥐고, 오도메트리 토픽만 `/odom`으로 바꿔 실행합니다.

```bash
python3 simple_safety_node.py --ros-args -p odom_topic:=/odom -p desired_speed:=0.5
```

코드는 동일합니다 — 무엇이 달라지고 왜 그런지는 본문 6.6절을 참고하세요.
