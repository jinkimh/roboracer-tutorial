#!/bin/bash
# F1TENTH Gym 시뮬레이터 Docker 실행 스크립트 (GPU 없는 환경, Ubuntu 22.04 / WSL 기준)
# 사전에 ~/f1tenth_ws/src 아래 f1tenth_gym_ros, f1tenth-software-stack을 clone하고
# 이미지를 build했다고 가정합니다. 컨테이너 내부는 ROS2 Foxy로 고정됩니다.

cd ~/f1tenth_ws || { echo "~/f1tenth_ws 디렉토리가 없습니다. README의 워크스페이스 생성 단계를 먼저 진행하세요."; exit 1; }

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
