# 시뮬레이터 오도메트리 튜닝 — sim_odom_calibrator

책 본문 [4.5절](../../../manuscript/04-차량모델링과좌표계/04-차량모델링과좌표계.md#45-🖥️-실습--시뮬레이터에서-오도메트리-튜닝해보기)과 짝을 이루는 실습입니다.
패키지 없이 `python3 sim_odom_calibrator.py`로 바로 실행할 수 있습니다.

f1tenth_gym_ros가 주는 오도메트리(`/ego_racecar/odom`)는 물리엔진이 계산한 정확한 값(ground truth)이라
그 자체로는 튜닝할 게 없습니다. 이 노드는 "만약 이 차에도 실차처럼 캘리브레이션이 필요한 가상 VESC가
달려 있다면?"을 흉내 냅니다 — `/drive` 명령을 실제 Roboracer 차량의 진짜 하드웨어 상수(코드 안에
숨겨둔 `HIDDEN_*` 값)로 인코딩한 뒤, 여러분이 ROS2 파라미터로 지정한 (일부러 살짝 틀린) 게인·오프셋으로
다시 디코딩해 `/odom_estimated`를 만들어냅니다.

## 실행

터미널 A — 2장에서 설치한 F1TENTH Gym 시뮬레이터 + 텔레옵을 켭니다.

터미널 B:

```bash
source /opt/ros/humble/setup.bash   # 사용 중인 배포판에 맞게
python3 sim_odom_calibrator.py
```

## 튜닝

새 터미널에서 ground truth와 추정치를 비교하며 파라미터를 조정합니다.

```bash
ros2 topic echo --once /ego_racecar/odom --field pose.pose.position   # ground truth
ros2 topic echo --once /odom_estimated --field pose.pose.position      # 추정치

ros2 param set /sim_odom_calibrator speed_to_erpm_gain 4400.0
ros2 param set /sim_odom_calibrator steering_angle_to_servo_offset 0.52
ros2 param set /sim_odom_calibrator steering_angle_to_servo_gain -1.15
```

정답(실제 Roboracer 차량의 기본값)은 `speed_to_erpm_gain=4614.0`,
`steering_angle_to_servo_gain=-1.2135`, `steering_angle_to_servo_offset=0.5304`입니다 — 4.7절 실차
튜닝에서 다시 만나는 값이니 미리 외울 필요는 없습니다. 자세한 절차는 본문 4.5절을 참고하세요.
