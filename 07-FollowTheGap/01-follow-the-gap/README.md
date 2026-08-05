# Follow-the-Gap — reactive_node

책 본문 [7.5절](../../../manuscript/07-FollowTheGap/07-FollowTheGap.md#75-🖥️-실습--follow-the-gap-노드-구현)(시뮬레이터)·
[7.7절](../../../manuscript/07-FollowTheGap/07-FollowTheGap.md#77-🚗-실습--실차-버전-레이스데이-준비와-파라미터-튜닝)(실차)과 짝을 이루는 실습입니다.
패키지 없이 `python3 reactive_node.py`로 바로 실행할 수 있습니다.

LiDAR 스캔 전체에서 "지금 가장 넓게 뚫린 방향"을 매 순간 스스로 찾아 조향하는 반응형 주행
(Follow-the-Gap) 노드입니다. 전처리(클리핑·`inf`/`nan` 방어) → 시야 제한(`fov_deg`) → 전역
최근접점 기준 버블마스킹 → 최대 갭 탐색 → 갭 중앙 조향 → 연속 속도 프로파일 순서로 동작합니다.
Wall Following(5장)과 달리 벽이라는 구조적 가정이 없어 임의의 장애물 배치에서도 동작하고, AEB(6장)
와는 결합하지 않는 독립 실행 노드입니다.

원본 자료는 [f1tenth/f1tenth_lab4_template](https://github.com/f1tenth/f1tenth_lab4_template)의
`reactive_node.py`(핵심 함수가 전부 미구현인 스켈레톤)와
[jinkimh/f1tenth-software-stack의 `reactive_node`](https://github.com/jinkimh/f1tenth-software-stack/blob/main/gap_follow/scripts/reactive_node.py)
(실제 레이스 코드)를 참고했지만, 둘 다 그대로 쓰지 않고 다시 작성했습니다(본문 7.2·7.5절에서
자세히 다룹니다).

- **인덱스 하드코딩 없음**: 실제 레이스 코드는 `data.ranges[180:899]`처럼 특정 LiDAR 사양에 맞춘
  슬라이스를 하드코딩하지만, 이 노드는 `scan.angle_min`/`scan.angle_increment`로 매번 계산합니다.
- **버블마스킹이 실제로 동작함**: 실제 레이스 코드는 버블마스킹 함수(`disparity_extender`)가
  정의만 되어 있고 호출되지 않습니다 — 이 노드는 전역 최근접점 기준 버블마스킹을 실제로 적용합니다.
- **연속 속도 프로파일**: 실제 레이스 코드는 조향각을 보지 않는 2단계 bang-bang 방식이지만, 이
  노드는 `v = clamp(v_min, v_max - k*|steering|, v_max)` 공식을 씁니다.

## 실행

```bash
source /opt/ros/humble/setup.bash   # 사용 중인 배포판에 맞게
python3 reactive_node.py
```

## 파라미터

| 이름 | 기본값 | 의미 |
|---|---|---|
| `max_range` | `4.0` | 이 거리(m)를 넘는 값은 클리핑 |
| `fov_deg` | `180.0` | 정면 기준 좌우 스캔 범위(도) |
| `bubble_radius_beams` | `20` | 전역 최근접점 앞뒤로 마스킹할 빔 개수 |
| `v_min` | `0.5` | 최대 조향각(`STEERING_LIMIT`)에서의 속도(m/s) |
| `v_max` | `3.0` | 직진(조향각 0)일 때의 속도(m/s) |

```bash
ros2 param set /reactive_node bubble_radius_beams 5
ros2 param set /reactive_node fov_deg 90.0
ros2 param set /reactive_node v_max 1.5
```

## 실차에서

4.7절 드라이버 스택을 먼저 브링업한 뒤, 조이스틱(비상 정지)을 손에 쥐고 `v_max`를 낮게 시작합니다.

```bash
python3 reactive_node.py --ros-args -p v_max:=1.0 -p v_min:=0.3
```

코드는 동일합니다 — 무엇이 달라지고 왜 그런지, 레이스데이 준비 절차는 본문 7.7절을 참고하세요.
