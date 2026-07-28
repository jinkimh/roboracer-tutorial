# roboracer-tutorial

[ROBORACER(F1TENTH)로 배우는 자율주행](https://github.com/jinkimh/roboracer-book) 책의 실습 자료 저장소입니다.
본문 원고는 별도 저장소(roboracer-book)에서 관리하고, 이 저장소에는 각 장의 🖥️/🚗 실습에 필요한
튜토리얼 문서와 코드만 모아둡니다. 책의 라이선스 정책상 본문 텍스트와 달리 이 저장소의 내용은
오픈소스(MIT)로 공개합니다.

## 구조

장별로 폴더를 나누고(`NN-장이름/`), 그 안에 실습(튜토리얼) 단위로 다시 폴더 또는 파일을 둡니다.

- 실습에 코드나 스크립트가 딸려 있으면 **폴더**로 관리합니다: `NN-실습이름/README.md` + 코드 파일들
- 별도 코드 없이 절차 설명만 있는 실습은 **파일 하나**(`NN-실습이름.md`)로 관리합니다

```
labs/
  02-ROS2기초와개발환경구축/
    01-f1tenth-gym-install/       # 코드(docker 스크립트)가 있어 폴더
      README.md
      docker_run.sh
    02-autodrive-install.md       # 코드 없이 설치 절차만 있어 파일 하나
    03-teleop-ros2-basics/        # 코드(예시 노드)가 있어 폴더
      README.md
      my_first_listener_node.py
```

## 라이선스

이 저장소의 모든 코드와 문서는 MIT 라이선스를 따릅니다. 자유롭게 재사용·수정·재배포할 수 있습니다.
