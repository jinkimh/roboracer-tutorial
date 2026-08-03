# 실차 오도메트리 튜닝 — vesc.yaml + 재빌드 스크립트

책 본문 [4.7절](../../../manuscript/04-차량모델링과좌표계/04-차량모델링과좌표계.md#step-4-odometry-튜닝) Step 4와 짝을 이루는 실습 자료입니다.
4.5절에서 시뮬레이터로 연습한 것과 같은 절차(관찰 → 조정 → 재실행 → 재확인)를 실제 차량의
`vesc.yaml`에 적용합니다. 원본 부트캠프 자료(`0-5-F110th_Odom_Tuning.md`)의 단계별 절차를 이 책의
구성에 맞춰 재정리했습니다[6].

## 파일

- **[vesc.yaml](vesc.yaml)**: `f1tenth_ws/src/f1tenth_system/f1tenth_stack/config/vesc.yaml`에 덮어쓸
  예시 설정. Roboracer 표준 차량의 기본값(4.4·4.5절에서 이미 만난 숫자)이 채워져 있지만, **여러분의
  차량에서 그대로 맞는다는 보장은 없습니다** — 아래 절차대로 반드시 직접 측정하고 조정하세요.
- **[rebuild_and_launch.sh](rebuild_and_launch.sh)**: `vesc.yaml`을 고칠 때마다 반복해야 하는
  `colcon build` → `source install/setup.bash` → `ros2 launch f1tenth_stack bringup_launch.py`
  세 단계를 한 번에 실행하는 스크립트.

> ⚠️ **`vesc.yaml`을 고칠 때마다 반드시 재빌드해야 합니다.** `colcon build` 없이 bringup만 다시
> 실행하면 변경 사항이 반영되지 않습니다 — 파라미터를 바꿨는데 차량 반응이 그대로라면 십중팔구 이걸
> 빼먹은 것입니다. 아래 세 단계를 손으로 치는 대신 `./rebuild_and_launch.sh`를 쓰세요.

## 1. 조향각 오프셋 (`steering_angle_to_servo_offset`) — 가장 먼저

**목적**: 차량이 똑바로 주행하도록 조향의 기본(중립) 위치를 보정합니다. 세 파라미터 중 반드시 가장
먼저 맞춰야 합니다 — 이게 틀어진 채로 ERPM 게인·조향각 게인을 조정하면, 직진이 안 되는 상태에서
거리·반경을 재게 되어 다음 두 단계의 측정값 자체가 부정확해집니다.

1. bringup을 실행하고 텔레옵으로 준비합니다.
   ```bash
   ros2 launch f1tenth_stack bringup_launch.py
   ```
2. 차량을 직선으로 주행시키고, 왼쪽/오른쪽 중 어느 방향으로 치우치는지 눈으로 확인합니다.
3. 치우친 방향에 따라 `vesc.yaml`의 값을 수정합니다.
   - 왼쪽으로 치우침 → `steering_angle_to_servo_offset` **증가**
   - 오른쪽으로 치우침 → `steering_angle_to_servo_offset` **감소**
4. `./rebuild_and_launch.sh`로 재빌드·재실행합니다.
5. 거의 똑바로 갈 때까지 2~4를 반복합니다.

일반적인 값 범위: **0.4 ~ 0.6**.

## 2. ERPM 게인 (`speed_to_erpm_gain`)

**목적**: 명령한 속도와 실제로 이동한 거리 사이의 오차를 줄입니다.

1. 줄자 등 측정 도구를 준비합니다(3m 이상 잴 수 있는 것).
2. 차량을 출발선에 0점 정렬한 뒤 bringup을 실행합니다.
3. 일정 거리를 직진 주행한 뒤, `/odom`이 보고하는 이동 거리를 확인합니다.
   ```bash
   ros2 topic echo --no-arr /odom
   ```
   (`--no-arr`는 배열 필드를 생략해 pose/twist 값만 간결하게 보여줍니다.)
4. `/odom`이 보고한 거리와 줄자로 잰 실제 거리를 비교해 게인을 조정합니다.
   - 보고된 거리 < 실제 거리 → 게인 **증가**
   - 보고된 거리 > 실제 거리 → 게인 **감소**
   - 조정 단위는 처음엔 **500** 정도로 크게 시작해서, 오차가 줄어들수록 더 작은 단위로 좁혀가세요.
5. `./rebuild_and_launch.sh`로 재빌드·재실행하고, 오차가 충분히 작아질 때까지 3~4를 반복합니다.

일반적인 값 범위: **2000 ~ 5000**.

### odom 값이 음수로 나온다면

일부 차량은 이 단계에서 `/odom`의 x값이 전진할수록 오히려 **감소**(음수 방향)하는 것을 보게 됩니다 —
속도 계산 부호가 반대로 되어 있다는 뜻이며, 파라미터 조정으로는 고칠 수 없는 코드 레벨의 문제입니다.
`f1tenth_system/vesc/vesc_ackermann/src/vesc_to_odom.cpp`의 속도 계산식(102번째 줄 부근)을 찾습니다.

```cpp
// 변경 전
double current_speed = (-state->state.speed - speed_to_erpm_offset_) / speed_to_erpm_gain_;
// 변경 후 — 전체를 -()로 한 번 더 감싸 부호를 반전
double current_speed = -(-state->state.speed - speed_to_erpm_offset_) / speed_to_erpm_gain_;
```

수정한 뒤에는 파라미터 변경이 아니라 **C++ 코드 변경**이므로 `colcon build`가 반드시 필요합니다. 체크리스트로
다시 정리하면:

- [ ] `ros2 topic echo /odom`에서 전진 시 x값이 감소하는가? (증가해야 정상)
- [ ] `vesc_to_odom.cpp`의 속도 계산식이 위 "변경 전" 형태인가?
- [ ] 전체 식을 `-()`로 한 번 더 감쌌는가?
- [ ] `colcon build`를 실행했는가?
- [ ] 재실행 후 전진 시 x값이 증가하는지 다시 확인했는가?

## 3. 조향각 게인 (`steering_angle_to_servo_gain`) — 마지막

**목적**: 정해진 회전 반경에 맞도록 조향 명령의 게인을 조정합니다. 오프셋(1단계)이 이미 맞춰져 있어야
회전 반경을 믿고 잴 수 있으므로 항상 마지막에 튜닝합니다.

1. 측정 테이프(또는 바닥에 표시한 격자) 위에 차량을 정렬합니다.
2. 최대 조향각 명령으로 원을 그리며 주행합니다.
3. 실제로 그려진 원의 반경을 측정합니다 — 원본 자료의 기준 차량은 목표값이 **1.722m**였습니다. 이
   숫자는 여러분 차량의 휠베이스·조향 한계에 따라 달라지므로, 절대값보다는 "일관되게 좁아지거나
   넓어지는지"를 기준으로 삼으세요.
4. 목표 반경에 못 미치면(원이 너무 좁으면) 게인을 **감소**, 넘어서면(원이 너무 넓으면) 게인을 **증가**시킵니다.
5. `./rebuild_and_launch.sh`로 재빌드·재실행하고, 반경이 충분히 가까워질 때까지 3~4를 반복합니다.

일반적인 값 범위: **1.1 ~ 1.3**.

## 요약

| 순서 | 파라미터 | 일반 범위 | 수정 후 필요한 작업 |
|---|---|---|---|
| 1 | `steering_angle_to_servo_offset` | 0.4 ~ 0.6 | `colcon build` + bringup 재실행 |
| 2 | `speed_to_erpm_gain` | 2000 ~ 5000 | `colcon build` + bringup 재실행 |
| — | odom 부호 반전(`vesc_to_odom.cpp`) | 해당 시에만 | `colcon build` (코드 변경이므로 필수) |
| 3 | `steering_angle_to_servo_gain` | 1.1 ~ 1.3 | `colcon build` + bringup 재실행 |

세 파라미터를 모두 맞춘 뒤 `ros2 topic echo /odom`으로 직진·회전 주행 시 값이 실제 움직임과 일치하는지
마지막으로 확인하세요 — 4.5절에서 시뮬레이터로 미리 연습했던 바로 그 확인 절차입니다.
