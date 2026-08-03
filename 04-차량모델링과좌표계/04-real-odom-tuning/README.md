# 실차 오도메트리 튜닝 — vesc.yaml + 재빌드 스크립트

책 본문 [4.7절](../../../manuscript/04-차량모델링과좌표계/04-차량모델링과좌표계.md#step-4-odometry-튜닝) Step 4와 짝을 이루는 실습 자료입니다.
4.5절에서 시뮬레이터로 연습한 것과 같은 절차(관찰 → 조정 → 재실행 → 재확인)를 실제 차량의
`vesc.yaml`에 적용합니다.

## 파일

- **[vesc.yaml](vesc.yaml)**: `f1tenth_ws/src/f1tenth_system/f1tenth_stack/config/vesc.yaml`에 덮어쓸
  예시 설정. Roboracer 표준 차량의 기본값(4.4·4.5절에서 이미 만난 숫자)이 채워져 있지만, **여러분의
  차량에서 그대로 맞는다는 보장은 없습니다** — 아래 절차대로 반드시 직접 측정하고 조정하세요.
- **[rebuild_and_launch.sh](rebuild_and_launch.sh)**: `vesc.yaml`을 고칠 때마다 반복해야 하는
  `colcon build` → `source install/setup.bash` → `ros2 launch f1tenth_stack bringup_launch.py`
  세 단계를 한 번에 실행하는 스크립트. `colcon build` 없이 bringup만 다시 실행하면 변경 사항이
  반영되지 않는다는 함정을 피하기 위한 것입니다.

## 튜닝 절차 (순서대로)

| 순서 | 파라미터 | 목적 | 절차 | 일반 범위 |
|---|---|---|---|---|
| 1 | `steering_angle_to_servo_offset` | 직진 주행 시 조향 중립점 보정 | 직진 주행 후 치우친 방향 확인 → 왼쪽 치우침이면 오프셋 증가, 오른쪽이면 감소 → 반복 | 0.4~0.6 |
| 2 | `speed_to_erpm_gain` | 명령 속도와 실제 이동 거리의 오차 축소 | 3m 이상 직진 후 `/odom` 이동 거리와 줄자 실측값 비교 → 보정 후 반복 | 2000~5000 |
| 3 | `steering_angle_to_servo_gain` | 목표 회전 반경에 맞게 조향 게인 조정 | 최대 조향각으로 원을 그리며 주행 후 반경 실측 → 미달 시 게인 감소, 초과 시 증가 | 1.1~1.3 |

```bash
# vesc.yaml 수정 후
./rebuild_and_launch.sh
```

## odom 부호 진단 체크리스트

일부 차량은 `/odom`의 x값이 음수로 나옵니다 — 속도 계산 부호가 반대로 되어 있다는 뜻입니다.

- [ ] `ros2 topic echo /odom`에서 전진 시 x값이 **감소**하는가? (증가해야 정상)
- [ ] 그렇다면 `f1tenth_system/vesc/vesc_ackermann/src/vesc_to_odom.cpp`의 속도 계산식을 확인 —
      `current_speed = (-state->state.speed - speed_to_erpm_offset_) / speed_to_erpm_gain_;` 형태인가?
- [ ] 위 식 전체를 `-()`로 한 번 더 감싸 부호를 반전시켰는가?
- [ ] 수정 후 `colcon build`(파라미터 변경이 아니라 C++ 코드 변경이므로 재빌드 필수)를 실행했는가?
- [ ] 재실행 후 전진 시 x값이 증가하는지 다시 확인했는가?
