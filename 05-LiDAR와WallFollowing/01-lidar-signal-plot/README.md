# LiDAR를 신호로 읽고 그려보기 — plot_scan

책 본문 [5.1절](../../../manuscript/05-LiDAR와WallFollowing/05-LiDAR와WallFollowing.md#🖥️-미니-실습--lidar를-신호로-읽고-그려보기) 미니 실습과 짝을 이룹니다.
패키지 없이 `python3 plot_scan.py`로 바로 실행할 수 있습니다.

`/scan`(`sensor_msgs/LaserScan`)을 한 번 구독해, (1) range-vs-angle "신호" 그래프와 (2) 극좌표를
직교좌표로 바꾼 "새의 눈 시점" 점군 산점도를 나란히 그립니다.

## 사전 준비

```bash
pip install matplotlib   # 아직 없다면
```

## 실행

2장에서 설치한 시뮬레이터(또는 4장에서 브링업한 실차)를 켜둔 상태에서:

```bash
source /opt/ros/humble/setup.bash   # 사용 중인 배포판에 맞게
python3 plot_scan.py
```

창이 뜨고 `scan_plot.png`로도 저장됩니다. 로봇을 벽 근처나 방 구석으로 옮긴 뒤 다시 실행해보면,
오른쪽 점군 그래프에서 방의 벽 모양이 그대로 드러나는 것을 볼 수 있습니다.
