# F1TENTH Gym 시뮬레이터 설치와 첫 실행 (Docker 기반)

책 본문 2.5절과 짝을 이루는 실습입니다. 개념 설명은 본문을 참고하고, 여기서는 명령어와 코드만 간결하게 정리합니다.

## 사전 준비

- Docker (`docker --version`으로 설치 확인)
- Ubuntu 22.04 또는 WSL(Ubuntu 22.04). NVIDIA GPU는 없어도 됩니다.

## Step 1. 워크스페이스 생성 및 저장소 clone

```bash
mkdir -p ~/f1tenth_ws/src
cd ~/f1tenth_ws/src
git clone https://github.com/jinkimh/f1tenth_gym_ros.git
git clone https://github.com/jinkimh/f1tenth-software-stack.git
```

## Step 2. Docker 이미지 빌드

```bash
cd ~/f1tenth_ws/src/f1tenth_gym_ros
docker build -t f1tenth_gym_ros -f Dockerfile .
```

## Step 3. 컨테이너 실행

[`docker_run.sh`](docker_run.sh)를 내려받아 실행하거나, 직접 아래 명령을 입력합니다.

```bash
cd ~/f1tenth_ws
xhost +local:docker
docker run -it \
  --privileged \
  --env="DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --volume="$HOME/f1tenth_ws/src/f1tenth_gym_ros:/sim_ws/src/f1tenth_gym_ros" \
  --volume="$HOME/f1tenth_ws/src/f1tenth-software-stack:/sim_ws/src/f1tenth-software-stack" \
  --name f110_gym_docker \
  f1tenth_gym_ros:latest
```

이후 재접속은 `docker start f110_gym_docker && docker exec -it f110_gym_docker bash`.

## Step 4. 빌드 및 실행

컨테이너 내부에서:

```bash
source /opt/ros/foxy/setup.bash
cd /sim_ws
colcon build
source install/setup.bash
ros2 launch f1tenth_gym_ros gym_bridge_launch.py
```

## 맵 바꾸기

기본 맵은 `levine`(실제 UPenn Levine Hall 테스트 트랙)입니다. `config/sim.yaml`의 `map_path`를
`.../maps/Spielberg_map`으로 바꾸고 다시 `colcon build` 후 재실행하면 실제 F1 서킷(레드불 링)을
1:10로 축소한 트랙으로 바뀝니다. 더 많은 실제 서킷 맵은 [f1tenth/f1tenth_racetracks](https://github.com/f1tenth/f1tenth_racetracks)를 참고하세요.

## 텔레옵

`sim.yaml`에 `kb_teleop: True`가 기본값입니다. 새 터미널에서:

```bash
docker exec -it f110_gym_docker bash
source /opt/ros/foxy/setup.bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

`i`(전진) `,`(후진) `u`/`o`(전진+좌/우) `m`/`.`(후진+좌/우) `k`(정지)

## 문제 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| RViz 창이 안 뜸 | X11 전달 실패 | 호스트에서 `xhost +local:docker` 재실행 |
| `docker: permission denied` | docker 그룹 미포함 | `sudo usermod -aG docker $USER` 후 재로그인 |
| 컨테이너 중복 생성 오류 | 이전 컨테이너 존재 | `docker start f110_gym_docker && docker exec -it f110_gym_docker bash`로 재접속 |
