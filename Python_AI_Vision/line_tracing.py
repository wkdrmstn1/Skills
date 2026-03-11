# UBUNTU PC에서만 가능 

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, CompressedImage

import cv2
import numpy as np


class LineTrace(Node):
    def __init__(self):
        super().__init__('line_trace_node')

        self.state = 'stop'
        self.line_detect = False
        self.obj_detect = False
        self.angular_z = 0.0

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # 카메라 딜레이 줄이기
        scan_qos = QoSProfile(
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT
        )

        self.lidar_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            scan_qos
        )

        self.image_sub = self.create_subscription(
            CompressedImage,
            '/image_raw/compressed',
            self.image_callback,
            10
        )

        self.timer = self.create_timer(0.1, self.control_loop)
        
    def detect_line(self, frame):
        height, width, _ = frame.shape
        roi = frame[height // 2 : height, :]            # 하단화면만 감지되도록  ROI 조정 

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # BLUE LINE
        lower_blue = np.array([100, 150, 80])
        upper_blue = np.array([140, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        ''' 
        # RED LINE
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)
        '''

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        M = cv2.moments(mask)

        if M['m00'] > 3000:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00']) + height // 2
            self.line_detect = True
        else:
            cX = width // 2
            cY = int(height * 0.75)
            self.line_detect = False

        offset = (width / 2) - cX
        self.angular_z = 0.01 * offset

        cv2.circle(frame, (cX, cY), 8, (0, 255, 0), -1)
        cv2.imshow('camera', frame)
        cv2.imshow('mask', mask)
        cv2.waitKey(1)

        

    def image_callback(self, msg):
        img_np = np.frombuffer(msg.data, dtype=np.uint8)
        frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        if frame is not None:
            self.detect_line(frame)

    def lidar_callback(self, msg):
        front = np.array(msg.ranges[160:200], dtype=float)
        front = np.nan_to_num(front, nan=1.0, posinf=1.0, neginf=1.0)

        self.obj_detect = np.min(front) <= 0.35

        if self.obj_detect:
            self.state = 'stop'
        else:
            self.state = 'trace' if self.line_detect else 'stop'

    def control_loop(self):
        twist = Twist()

        if self.state == 'trace':
            twist.linear.x = 0.12
            twist.angular.z = float(self.angular_z)
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        self.cmd_pub.publish(twist)

        self.get_logger().info(
            f"STATE: {self.state} | LINE: {self.line_detect} | OBSTACLE: {self.obj_detect}"
        )


def main():
    rclpy.init()
    node = LineTrace()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
