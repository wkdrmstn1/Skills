from ultralytics import YOLO

if __name__ == '__main__':
    # 1. 모델 불러오기 (가벼운 버전 n)
    model = YOLO('yolov8n.pt') 

    # 2. 훈련 시작
    # data='data.yaml' -> 현재 폴더에 있는 설정 파일 사용
    # epochs=30 -> 30번 반복 공부 (컴퓨터 느리면 10으로 줄이세요)
    # imgsz=416 -> 이미지 크기 (속도와 정확도 균형)
    model.train(data='data.yaml', epochs=30, imgsz=416, device='cpu')