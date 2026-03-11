import cv2
import roslibpy
import numpy as np
import base64
import time

ROSBRIDGE_IP = '192.168.0.138'
ROSBRIDGE_PORT = 9090

client = roslibpy.Ros(host=ROSBRIDGE_IP, port=ROSBRIDGE_PORT)

try:
    client.run()
    print('Connected to ROS')
except Exception as e:
    print(e)
    exit()

def image_callback(msg):
    try:
        img_data = base64.b64decode(msg['data'])
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        cv2.imshow("TurtleBot View", frame)
        cv2.waitKey(1)
    except Exception as e:
        print(e)

listener = roslibpy.Topic(client, '/cv_bridge','sensor_msgs/msg/CompressedImage')
listener.subscribe(image_callback)


try:
    while client.is_connected:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    listener.unsubscribe()
    client.terminate()
    cv2.destroyAllWindows()