from ultralytics import YOLO
import numpy as np
import roslibpy
import time
import threading
import cv2
import math

IP = '192.168.0.138'
PORT = 9090
ros = roslibpy.Ros(host=IP, port=PORT)

try:
    ros.run()
    print('Connected to ROS')
except Exception as e:
    print(e)
    exit()

try:
    model = YOLO("case\runs\detect\train\weights\best.pt")
    #model = YOLO("yolov8n.pt")
    print("YOLO Model Loaded")
except Exception as e:
    print(e)
    exit()

GET_TB3_DIRECTION = 0
TB3_DRIVE_FORWARD = 1
TB3_RIGHT_TURN = 2
TB3_LEFT_TURN = 3

CENTER = 0
LEFT = 1
RIGHT = 2

LINEAR_VELOCITY = 0.15
ANGULAR_VELOCITY = 0.5
DEG2RAD = math.pi / 180.0
SAFE_DISTANCE = 0.7

scan_data = [10.0, 10.0, 10.0]
object_detected = False
running = True

def scan_callback(msg):
    global scan_data
    ranges = np.array(msg.get('ranges', []), dtype=np.float32)
    
    if len(ranges) >= 360:
        ranges = np.nan_to_num(ranges, posinf=10.0, neginf=0.0, nan=10.0)
        ranges[ranges == 0.0] = 10.0

        front_cone = np.concatenate([ranges[:20], ranges[-20:]])
        left_cone = ranges[70:110]
        right_cone = ranges[250:290]

        scan_data[CENTER] = np.min(front_cone)
        scan_data[LEFT] = np.min(left_cone)
        scan_data[RIGHT] = np.min(right_cone)

def cam_loop():
    global object_detected
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while running:
        ret, frame = cap.read()
        if not ret: continue

        results = model(frame, imgsz=416, verbose=False, conf=0.3)
        
        if len(results[0].boxes) > 0:
            object_detected = True
        else:
            object_detected = False
            
        cv2.imshow("YOLO Cam", results[0].plot())
        if cv2.waitKey(1) == 27: break
        time.sleep(0.05)
    
    cap.release()
    cv2.destroyAllWindows()

listener_scan = roslibpy.Topic(ros, '/scan', 'sensor_msgs/LaserScan', throttle_rate=100)
listener_scan.subscribe(scan_callback)

talker = roslibpy.Topic(ros, '/cmd_vel', 'geometry_msgs/Twist', queue_length=1)
talker.advertise()

def send_velocity(linear, angular):
    cmd = roslibpy.Message({
        'linear': {'x': linear, 'y': 0.0, 'z': 0.0},
        'angular': {'x': 0.0, 'y': 0.0, 'z': angular}
    })
    talker.publish(cmd)

def control_loop():
    global object_detected
    
    was_stopped = False

    while running:
        if scan_data[CENTER] != 10.0: break
        time.sleep(0.5)

    while running:
        if object_detected:
            send_velocity(0.0, 0.0)
            was_stopped = True
            time.sleep(0.1)
            continue

        if was_stopped:
            was_stopped = False

        if scan_data[CENTER] < SAFE_DISTANCE:
            if scan_data[LEFT] > scan_data[RIGHT]:
                send_velocity(0.0, ANGULAR_VELOCITY)
            else:
                send_velocity(0.0, -ANGULAR_VELOCITY)
        else:
            send_velocity(LINEAR_VELOCITY, 0.0)
        
        time.sleep(0.1)

t_cam = threading.Thread(target=cam_loop)
t_cam.start()

t_control = threading.Thread(target=control_loop)
t_control.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    running = False
    t_cam.join()
    t_control.join()

finally:
    running = False
    send_velocity(0.0, 0.0)
    
    cv2.destroyAllWindows()
    talker.unadvertise()
    listener_scan.unsubscribe()
    ros.terminate()