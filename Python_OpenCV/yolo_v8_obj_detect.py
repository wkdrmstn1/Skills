from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

model = YOLO("yolov8n.pt")  # 사용할 모델 다운로드하여 인스턴스 생성
img = cv2.imread('image\office.jpg')

# 이미지 추론 
results = model(img, conf = 0.5)

for result in results :
    print(result.boxes)     # 감지한 boxes 정보 출력 
    boxes = result.boxes
    for box in boxes :
        c = box.cls[0]          # 클래스 번호 
        conf = box.conf[0]         # 점수(정확도? 유사도?) 
        x1, y1, x2, y2 = box.xyxy[0]         # box의 좌표 
        
        # 클래스 이름 알아내기 (names 딕셔너리 활용)
        class_name = model.names[int(c)]
        
        print(f"물체: {class_name}, 확신도: {conf :.2f}")
        print(f"좌표: ({x1:.1f}, {y1:.1f}) ~ ({x2:.1f}, {y2:.1f})")
        print("-" * 30)

# 시각화 된 이미지 보기
annotated_frame = results[0].plot()
cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
cv2.imshow("result", annotated_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()


