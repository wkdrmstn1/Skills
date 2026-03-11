import cv2
import numpy as np 

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

classes = []
with open("sample.names", "r") as f :
    classes = [line.strip() for line in f.readlines()]

# 출력층 따로 구분해서 리스트화
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

colors = np.random.uniform(0, 255, size=(len(classes), 3))
camera = cv2.VideoCapture(0)


while True:
    class_ids = []
    confidences = []
    boxes = []

    delay = int(camera.get(cv2.CAP_PROP_FPS))
    
    ret, frame = camera.read()
    height, width, channels = frame.shape

    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id] # 최종 점수
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # 어디가 좌상단인지 좌표
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # 중복되는 내용을 억제하는 함수 
    # 0.5 의 의미 : 이 점수보다 낮은 건 제거하는!
    # 0.4 의 의미 : 박스 간에 겹치는 비율이 0.4 이상이면 제거하는! 
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            obj_id = class_ids[i]
            label = str(classes[class_ids[i]])
            color = colors[obj_id]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y + 30), font, 3, color, 3)
    
    cv2.imshow("Webcam Image", frame)

    keyboard_input = cv2.waitKey(delay)
    if keyboard_input == 27:
        break

cv2.destroyAllWindows()