# ROS2 Vision & AI Robot System (Ros2_pkg)

**CvBridge**를 사용하여 ROS 2의 이미지 메시지를 OpenCV 및 YOLOv8과 결합하여 학습 

## 📂 패키지 구성 (Package Structure)

| 파일명 | 주요 기능 및 역할 | 핵심 기술 (Bridge) |
|:---:|:---|:---:|
| **cv_bridge_yolo.py** | **비전 인식 주행**: 실시간 이미지 변환 및 YOLOv8 객체 인식 | **CvBridge**, YOLOv8 |
| **cv_bridge_cam.py** | **모니터링**: ROS 2 이미지 스트림을 OpenCV 윈도우로 시각화 | **CvBridge**, OpenCV |
| **basic_drive.py** | **자율주행**: A* 경로 계획 및 Pure Pursuit 추종 | A*, Pure Pursuit |
| **turtlebot3_drive.py** | **상태 제어**: 상태 머신(FSM) 기반의 장애물 회피 | Odom, FSM |
| **best.pt / yolov8n.pt** | 객체 인식을 위한 AI 가중치 모델 | Deep Learning |

---

## 🛠️ 핵심 기술: CvBridge 데이터 파이프라인

이 프로젝트의 핵심은 ROS 2 네트워크의 **비정형 이미지 메시지**를 인공지능이 이해할 수 있는 **데이터 형식**으로 가공하는 것입니다.

### 1. 이미지 변환 프로세스 (Vision Bridge)
* **Message Conversion**: ROS 2의 `sensor_msgs/Image` 데이터를 **CvBridge**를 통해 OpenCV의 `bgr8` 포맷(Numpy 배열)으로 실시간 변환합니다.
* **AI Inference**: 변환된 프레임을 YOLOv8 모델에 입력하여 "휴대폰" 등 특정 객체의 좌표와 클래스를 추출합니다.
* **Safety Control**: 인식된 결과에 따라 로봇의 속도를 제어하거나 긴급 정지(`stop_robot`) 명령을 하달합니다.



### 2. 고효율 모니터링 시스템
* **Real-time Monitoring**: 로봇이 보고 있는 화면을 지연 시간 없이 모니터링하기 위해 CvBridge를 통한 최적화된 스트리밍 구조를 채택했습니다.
* **Data Visualization**: 인식된 객체 위에 바운딩 박스를 그리고 레이블을 표시하여 현재 인식 상태를 시각적으로 검증합니다.

---

## 🚀 주행 및 제어 알고리즘

### 1. 전역/지역 경로 계획 (Navigation)
* **A* Planner**: 격자 지도를 분석하여 최적의 이동 경로를 탐색합니다.
* **Pure Pursuit**: 전방 주시 거리를 추적하며 부드러운 조향 곡선을 생성합니다.

### 2. 반응형 장애물 회피 (Reactive Control)
* **LiDAR Sensing**: 라이다 데이터를 분석하여 맵에 없는 장애물 발견 시 즉각 회피합니다.
* **Odometry Feedback**: 쿼터니언 기반의 위치 정보를 Yaw 각도로 변환하여 정밀한 헤딩 제어를 수행합니다.

---

## 🏃 실행 방법 (Usage)

### 1. 빌드 및 환경 설정
```bash
$ colcon build --symlink-install$ source install/setup.bash
$ ros2 run ros2_pkg cv_bridge_yolo
$ ros2 run ros2_pkg cv_bridge_cam
$ ros2 run ros2_pkg basic_drive
$ ros2 run ros2_pkg turtlebot3_drive
```
