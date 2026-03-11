import cv2 
import numpy as np 
import roslibpy
import base64

IP = '192.168.0.138'
PORT = 9090
ros = roslibpy.Ros(host=IP, port=PORT)
ros.run()

talker = roslibpy.Topic(ros, '/cmd_vel', 'geometry_msgs/Twist')
talker.advertise()

current_frame = None

def image_callback(msg):
    global current_frame
    encoded_data = msg['data']
    decoded_data = base64.b64decode(encoded_data)
    np_arr = np.frombuffer(decoded_data, np.uint8)
    current_frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

camera_topic = roslibpy.Topic(ros, '/image_raw/compressed','sensor_msgs/msg/CompressedImage')
camera_topic.subscribe(image_callback)

try:
    while True:
        if current_frame is None:
            continue

        frame = current_frame.copy()
        frame = cv2.resize(frame, (320, 240))
        height, width, channels = frame.shape

        lower_bound = np.array([100, 100, 50])
        upper_bound = np.array([140, 255, 255])

        mask = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), lower_bound, upper_bound)
        
        M = cv2.moments(mask)

        linear_x = 0.0
        angular_z = 0.0

        if M["m00"] > 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            offset = (width // 2) - cX

            if abs(offset) < 30:
                linear_x = 0.1
                angular_z = 0.0
                print(f"go {offset}")
            else: 
                linear_x = 0.05
                angular_z = offset * 0.003
                print(f"turn {offset}")

            cv2.circle(frame, (cX, cY), 10, (0, 0, 255), -1)

        else:
            linear_x = 0.0
            angular_z = 0.0
        
        cmd_vel = roslibpy.Message({
            'linear': {'x': linear_x, 'y': 0.0, 'z': 0.0},
            'angular': {'x': 0.0, 'y': 0.0, 'z': angular_z}
        })
        talker.publish(cmd_vel)
    
        cv2.imshow("Mask", mask)
        cv2.imshow("Turtlebot View", frame)

        if cv2.waitKey(1) == 27:
            break

except KeyboardInterrupt:
    pass

finally:
    stop_cmd = roslibpy.Message({
        'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0},
        'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
    })
    talker.publish(stop_cmd)
    
    cv2.destroyAllWindows()
    talker.unadvertise()
    camera_topic.unsubscribe()
    ros.terminate()