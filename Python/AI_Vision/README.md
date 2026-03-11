# 🤖 AI Vision & Robot Control

이 폴더는 인공지능(YOLO) 객체 인식과 로봇의 센서(LiDAR, Camera) 데이터를 결합하여 **자율주행 및 원격 제어 시스템**을 구현한 핵심 코드들을 포함하고 있습니다.

## 📂 파일별 기능 요약 (File Description)

### 1. 🚗 자율주행 및 비전 AI 융합 (Autonomous & Vision Control)
카메라 영상 분석(OpenCV/YOLO)과 라이다(LiDAR) 센서를 결합한 로봇 제어 코드입니다.

| 파일명 | 주요 기능 및 학습 내용 |
| :--- | :--- |
| **`turtlebot_drive.py`** | LiDAR(`/scan`) 및 오도메트리 데이터를 활용한 상태 머신(FSM) 기반의 기본 장애물 회피 주행 (rclpy) |
| **`turtlebot_drive_cam.py`** | 로컬 PC 웹캠으로 YOLO 객체 인식을 수행하며, 동시에 LiDAR 데이터로 장애물을 회피하는 융합 주행 (roslibpy) |
| **`turtlebot_drive_turtlecam.py`** | 로봇(Turtlebot) 시점의 카메라 영상을 수신하여 YOLO 객체 인식 후 반응(정지/주행)하는 원격 통합 제어 |
| **`line_tracing.py`** | 카메라 영상(HSV, ROI)으로 차선을 인식해 조향하고, LiDAR로 전방 장애물 감지 시 정지하는 복합 제어 노드 (rclpy) |
| **`line_detect_cam.py`** | 압축 이미지 토픽을 구독해 OpenCV 이미지 모멘트(Moments)로 중심점 오차를 계산하고 라인트레이싱 수행 |

### 2. 📡 센서 데이터 시각화 및 서버 통신 (Sensor Data & Network)
LiDAR 데이터의 좌표 변환 및 시뮬레이션, 그리고 외부 통신을 위한 서버 코드입니다.

| 파일명 | 주요 기능 및 학습 내용 |
| :--- | :--- |
| **`lidar_data_read.py`** | 웹소켓(`roslibpy`)을 통해 LiDAR 데이터를 수신하고 Matplotlib으로 실시간 시각화 및 충돌 방지 제어 |
| **`make_lidar_data(F).py`** | 극좌표계(거리, 각도)를 직교좌표계(X, Y)로 변환하여 360도 가상의 LiDAR 데이터를 생성 및 시각화 |
| **`make_lidar_data_roi(F).py`** | 가상 LiDAR 데이터 중 특정 관심 영역(ROI, 특정 거리 및 각도)의 데이터만 필터링하여 시각화 |
| **`flask_react_test.py`** | 로봇 상태 모니터링 및 웹 앱 연동을 위해 CORS를 허용한 간단한 Flask REST API 테스트 서버 |

### 3. 📸 데이터 수집 및 기타 (Data Collection)
딥러닝 모델 학습을 위한 데이터 수집 유틸리티입니다.

| 파일명 | 주요 기능 및 학습 내용 |
| :--- | :--- |
| **`img_make.py`** | 웹캠을 구동하고 키보드 입력('c') 시 프레임을 캡처하여 딥러닝 학습용 이미지 파일로 저장하는 스크립트 |