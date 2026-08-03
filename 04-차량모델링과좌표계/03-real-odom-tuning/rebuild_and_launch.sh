#!/usr/bin/env bash
# rebuild_and_launch.sh — vesc.yaml을 고칠 때마다 반복하는 3단계를 한 번에 실행
#
# 책 본문 4.7절 Step 4: "colcon build 없이 bringup만 다시 실행하면 변경
# 사항이 적용되지 않습니다"라는 함정을 피하기 위한 스크립트입니다.
# 사용법: vesc.yaml을 수정한 뒤 이 스크립트를 실행하세요.
set -e

cd ~/f1tenth_ws
colcon build --packages-select f1tenth_stack
source install/setup.bash
ros2 launch f1tenth_stack bringup_launch.py
