from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

camera = cv2.VideoCapture(0)
model = YOLO("yolov8n.pt")  # 사용할 모델 다운로드하여 인스턴스 생성

# 이미지 추론 
while True:
    ret, frame = camera.read()
    frame = cv2.flip(frame,1)
    results = model(frame, conf = 0.6)

    for result in results : 
        boxes = result.boxes

        for box in boxes :
            c = box.cls[0]          # 클래스 번호 
            conf = box.conf[0]         # 점수(정확도? 유사도?) 
            x1, y1, x2, y2 = map(int, box.xyxy[0])   # box의 좌표 
            
            # 클래스 이름 알아내기 (names 딕셔너리 활용)
            class_name = model.names[int(c)]
            
            print(f"물체: {class_name}, 확신도: {conf :.2f}")
            print(f"좌표: ({x1:.1f}, {y1:.1f}) ~ ({x2:.1f}, {y2:.1f})")
            print("-" * 30)

    # 시각화 된 이미지 보기
    annotated_frame = results[0].plot()
    
    cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
    
    if class_name == 'cell phone':
        text = 'Warning'
        cv2.putText(annotated_frame, text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("result", annotated_frame)
    
    keyboard_input = cv2.waitKey(50)
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()


