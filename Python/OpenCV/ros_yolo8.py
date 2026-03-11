from ultralytics import YOLO
import cv2
import roslibpy
import numpy as np
import base64

ROSBRIDGE_IP = '192.168.0.138'
ROSBRIDGE_PORT = 9090

client = roslibpy.Ros(host=ROSBRIDGE_IP, port=ROSBRIDGE_PORT)

try:
    client.run()
    print('Connected to ROS')
except Exception as e:
    print(e)
    exit()

model = YOLO("yolov8n.pt")
current_frame = None

def image_callback(msg):
    global current_frame
    try:
        img_data = base64.b64decode(msg['data'])
        np_arr = np.frombuffer(img_data, np.uint8)
        current_frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        print(e)

listener = roslibpy.Topic(client, '/image_raw/compressed','sensor_msgs/msg/CompressedImage')
listener.subscribe(image_callback)

print("Waiting data...")

while True:
    if current_frame is None:
        cv2.waitKey(10)
        continue
    
    frame_to_process = current_frame.copy()
    results = list(model(frame_to_process, stream=True, conf=0.6, verbose=False))
    annotated_frame = results[0].plot()

    is_cellphone = False

    for result in results:
        boxes = result.boxes
        for box in boxes:
            c = int(box.cls[0])
            class_name = model.names[c]
            
            if class_name == 'cell phone':
                is_cellphone = True

    if is_cellphone:
        text = 'Warning!'
        cv2.putText(annotated_frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("result", annotated_frame)
    
    if cv2.waitKey(30) == 27:
        break

listener.unsubscribe()
client.terminate()
cv2.destroyAllWindows()