#  roslibpy를 이용한 토픽 구독 및 발행
import numpy as np
import matplotlib.pyplot as plt 
import roslibpy
import time

# ros 기기와 연결 웹소켓 서버 열기
IP = '192.168.0.138'
PORT = 9090

ros = roslibpy.Ros(host=IP, port=PORT)

plt.ion()
fig, ax = plt.subplots(figsize=(6,6))
ros.run()

# lidar 센서 토픽 받기 -> ros 기기에서 /scan 토픽 발행중 이어야 함
# -> ro2 launch turtlebot3_bringup robot.launch.py
x = np.array([])
y = np.array([])
front_dist = 10.0
def callback(msg):
    global x, y, front_dist

    ranges = np.array(msg['ranges'], dtype=np.float32)
    ranges = np.nan_to_num(ranges, posinf=10.0, neginf=0.0, nan=10.0)
    
    if len(ranges) > 60:
        front_ranges = np.concatenate([ranges[:30], ranges[-30:]])
        front_dist = np.min(front_ranges)

    angle_min = msg['angle_min']
    angle_increment = msg['angle_increment']
    angles = angle_min + np.arange(len(ranges)) * angle_increment
    angles = angles + np.pi/2       # turtlebot 방향 변경

    x = ranges * np.cos(angles)
    y = ranges * np.sin(angles)


listener = roslibpy.Topic(ros, "/scan", "sensor_msgs/msg/LaserScan")
listener.subscribe(callback)

talker = roslibpy.Topic(ros, '/cmd_vel', 'geometry_msgs/msg/Twist')
talker.advertise()

try:
    while True:
        time.sleep(0.1)

        if front_dist <= 0.5:
            cmd_vel = roslibpy.Message({
                'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0},
                'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
            })
            talker.publish(cmd_vel)
            print("stop")

        else:
            cmd_vel = roslibpy.Message({
                'linear': {'x': 0.1, 'y': 0.0, 'z': 0.0},
                'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
            })
            talker.publish(cmd_vel)
            print("go")
        
        ax.clear()
        ax.scatter(0, 0, color="blue", label="turtlebot3",marker='^',zorder = 10, s = 100)
        ax.scatter(x, y, color="red", label="LiDar Points")
        ax.legend()

        plt.draw()
        plt.pause(0.5)

except KeyboardInterrupt:
    listener.unadvertise()
    talker.unadvertise()
    ros.terminate()