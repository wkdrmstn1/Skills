
OpenCV를 활용한 기초 영상 처리부터 얼굴 인식, 딥러닝(YOLO, Keras) 기반의 객체 탐지, 그리고 ROS 2 환경과의 비전 데이터 통신까지
아우르는 **컴퓨터 비전 종합 학습 코드**를 학습했습니다

## 📂 파일별 기능 요약 (File Description)

### 1. 🎨 기초 영상 처리 및 이벤트 제어 (OpenCV Basics)
이미지 이진화, 모폴로지 연산, 합성 등 OpenCV의 핵심 기능과 마우스 콜백 이벤트를 다룹니다.

| 파일명 | 주요 기능 및 학습 내용 |
| :--- | :--- |
| **`contours.py`** | 이미지 그레이스케일 변환 및 이진화(Threshold) 후 객체의 외곽선(Contour) 검출 |
| **`count_coins.py`** | 가우시안 블러와 모폴로지 연산(Closing)으로 노이즈를 제거하고 동전 개수 자동 카운팅 |
| **`erode+dilate.py`** | 이미지의 침식(Erosion) 및 팽창(Dilation) 등 객체 형태를 보정하는 기본 모폴로지 연산 |
| **`lena+chroma.py`** | 특정 색상 영역(`inRange`) 추출 및 비트 연산(`bitwise`)을 활용한 크로마키 이미지 합성 |
| **`motion_detect.py`** | 연속된 프레임 간의 픽셀 차이(`absdiff`)를 계산하여 실시간 움직임 감지 |
| **`paint.py`** | OpenCV 마우스 콜백 이벤트를 활용한 인터랙티브 그림판 구현 |
| **`apple_tomato.py`** | 이미지 폴더에서 데이터를 읽어와 리사이징하고, 머신러닝 학습용 NumPy 배열로 전처리 |

### 2. 👤 얼굴 인식 및 AR 필터 (Face Detection & AR)
사전 학습된 모델을 활용하여 사람의 얼굴을 인식하고 이미지를 덧씌우는 응용 기술입니다.

| 파일명 | 주요 기능 및 학습 내용 |
| :--- | :--- |
| **`haarac_image.py`** | 사전 학습된 Haar Cascade 분류기를 이용하여 정적 이미지 내 얼굴 영역 탐지 및 박스 표시 |
| **`filter.py`** | 실시간 웹캠 영상에서 얼굴을 추적하고, 검출된 위치에 투명도(Alpha)가 포함된 AR 스티커 합성 |

### 3. 🧠 딥러닝 기반 객체 인식 (YOLO & Keras)
신경망 모델을 활용하여 이미지나 실시간 영상 속의 다양한 사물을 분류하고 탐지합니다.

| 파일명 | 주요 기능 및 학습 내용 |
| :--- | :--- |
| **`yolo_v3.py`** | OpenCV `dnn` 모듈을 활용하여 정적 이미지에서 YOLOv3 기반 객체 탐지 및 NMS 알고리즘 적용 |
| **`yolo_v3_obj_detect_camera.py`** | 웹캠 영상을 통해 실시간으로 YOLOv3 객체 탐지 및 바운딩 박스 시각화 |
| **`yolo_v8_obj_detect.py`** | `ultralytics` 라이브러리를 활용한 최신 YOLOv8 기반 정적 이미지 객체 탐지 |
| **`yolo_v8_obj_detecr_camera.py`** | 웹캠 기반 실시간 YOLOv8 객체 탐지 및 특정 객체(휴대폰 등) 감지 시 경고 알림 표시 |
| **`obj_detect_image.py`** | 사전 학습된 Keras 모델(`.h5`)을 이용한 정적 이미지 분류 및 확신도(Confidence) 산출 |
| **`obj_detect_camera.py`** | 실시간 웹캠 영상을 전처리하여 Keras 모델을 통한 실시간 사물 분류 수행 |

### 4. 📡 ROS 2 연동 및 네트워크 통신 (ROS Bridge & Server)
비전 데이터를 외부 서버나 ROS 2 생태계와 주고받는 통신 코드입니다.

| 파일명 | 주요 기능 및 학습 내용 |
| :--- | :--- |
| **`cv_sub.py`** | 웹소켓(`roslibpy`)을 통해 ROS 2의 압축 이미지 토픽을 구독하고 OpenCV 프레임으로 디코딩하여 출력 |
| **`ros_yolo8.py`** | ROS 2 기기에서 전송하는 실시간 카메라 영상 토픽을 수신하여 즉각적으로 YOLOv8 객체 추론 수행 |
| **`test.py`** | Python `requests`를 이용하여 외부 Flask API 서버로 이미지 파일과 위치/상태 데이터를 POST 전송 |