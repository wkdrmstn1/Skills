# ROS2 Workspace - Study & Test Repository

ROS2 Humble 환경에서 로봇 제어, 슬램(SLAM), 파라미터 및 QoS 설정을 학습

## 📂 주요 패키지 구성 (Packages)

| 패키지명 | 주요 테스트 내용 |  
|:---:|:---|
| **3d_pkg** | 3D 센서 데이터 처리 및 가상 환경 테스트 |
| **my_param_pkg** | ROS2 Parameter 선언 및 동적 변경 테스트 |
| **qos_pkg** | 데이터 신뢰성 및 통신 정책 비교 테스트 | 
| **slam_pkg** | 지도 생성 및 SLAM 알고리즘 적용 테스트 | 
| **my_turtle_pkg** | 거북이(Turtlesim) 제어 및 기초 인터페이스 테스트 | 
| **maps** | 슬램을 통해 생성된 지도 데이터 저장 폴더 |

## 🚀 주요 기능 및 실습 내용

1. **Slam Test**: LiDAR 데이터를 활용한 지도 생성 및 저장
2. **QoS (Quality of Service)**: Best Effort, Reliable 등 통신 정책에 따른 데이터 수집 안정성 검증
3. **Launch File Test**: 여러 노드를 한 번에 실행하기 위한 런치 파일 구조 설계
4. **Param Test**: 노드 실행 중 파라미터를 통한 설정값 제어 실습

## 🛠️ 실행 방법 (Usage)

```bash
# 워크스페이스 빌드
$ colcon build --symlink-install

# 환경 설정
$ source install/setup.bash

# 특정 패키지 실행 
$ ros2 run [패키지명] [파일명]

# 특정 패키지 실행 (런치 파일일 경우)
$ ros2 launch [패키지명] [런치파일명].launch.py
