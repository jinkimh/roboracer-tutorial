# TF 최소 예제 — Broadcaster/Listener

책 본문 3.3절과 짝을 이루는 실습입니다. 패키지 없이 `python3 파일이름.py`로 바로 실행할 수
있습니다. `base_link` 기준 0.275m 앞에 `laser` 좌표계가 있다고 정적(static) TF를
발행/조회합니다 — 값은 2장에서 설치한 F1TENTH Gym의 `scan_distance_to_base_link`와 같습니다.

```bash
source /opt/ros/humble/setup.bash   # 사용 중인 배포판에 맞게
python3 minimal_tf_broadcaster.py
```

새 터미널에서:

```bash
python3 minimal_tf_listener.py
# 또는
ros2 run tf2_ros tf2_echo base_link laser
```

`tf2_echo`가 `Translation: [0.275, 0.0, 0.0]` 근처 값을 출력하면 성공입니다.

패키지로 정식 등록하고 launch로 다른 노드들과 함께 실행하는 전체 과정은
[03-ros2-basics-workspace](../03-ros2-basics-workspace/)(책 본문 3.7절)에서 다룹니다.
