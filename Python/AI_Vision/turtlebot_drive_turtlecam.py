from ultralytics import YOLO
import numpy as np
import roslibpy
import time
import threading
import cv2
import base64

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
    #model = YOLO("case\runs\detect\train\weights\best.pt")
    model = YOLO("yolov8n.pt")
    print("YOLO Model Loaded")
except Exception as e:
    print(e)

GET_TB3_DIRECTION = 0
TB3_DRIVE_FORWARD = 1
TB3_RIGHT_TURN = 2
TB3_LEFT_TURN = 3

CENTER = 0
LEFT = 1
RIGHT = 2

LINEAR_VELOCITY = 0.15
ANGULAR_VELOCITY = 0.5
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

def image_callback(msg):
    global object_detected
    
    encoded_data = msg['data']
    decoded_data = base64.b64decode(encoded_data)
    np_arr = np.frombuffer(decoded_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is None: return

    results = model(frame, imgsz=320, verbose=False, conf=0.5)
    
    if len(results[0].boxes) > 0:
        object_detected = True
        print("Object Detected", end='\r')
    else:
        object_detected = False
        
    cv2.imshow("Turtlebot Camera", results[0].plot())
    cv2.waitKey(1)

listener_scan = roslibpy.Topic(ros, '/scan', 'sensor_msgs/LaserScan', throttle_rate=100)
listener_scan.subscribe(scan_callback)

listener_cam = roslibpy.Topic(ros, '/image_raw/compressed', 'sensor_msgs/CompressedImage', throttle_rate=100)
listener_cam.subscribe(image_callback)

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

t_control = threading.Thread(target=control_loop)
t_control.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    running = False
    t_control.join()

finally:
    running = False
    send_velocity(0.0, 0.0)
    
    cv2.destroyAllWindows()
    talker.unadvertise()
    listener_scan.unsubscribe()
    listener_cam.unsubscribe()
    ros.terminate()
    print("Exit")