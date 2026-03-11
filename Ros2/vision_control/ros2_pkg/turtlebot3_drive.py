import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import numpy as np


GET_TB3_DIRECTION = 0
TB3_DRIVE_FORWARD = 1
TB3_RIGHT_TURN = 2
TB3_LEFT_TURN = 3

CENTER = 0
LEFT = 1
RIGHT = 2

LINEAR_VELOCITY = 0.22
ANGULAR_VELOCITY = 1.5
DEG2RAD = math.pi / 180.0

class Turtlebot3Drive(Node):
    def __init__(self):
        super().__init__('turtlebot3_drive_node')

        self.scan_data = [0.0, 0.0, 0.0]
        self.robot_pose = 0.0
        self.prev_robot_pose = 0.0
        self.turtlebot3_state_num = GET_TB3_DIRECTION

        qos = QoSProfile(depth=10)
        
        sensor_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', qos)
        
        self.scan_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            sensor_qos)
            
        self.odom_sub = self.create_subscription(
            Odometry,
            'odom',
            self.odom_callback,
            qos)

        self.update_timer = self.create_timer(0.01, self.update_callback)

        self.get_logger().info("Turtlebot3 simulation node has been initialised")

    def get_yaw_from_quaternion(self, q):
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        return yaw

    def odom_callback(self, msg):
        orientation = msg.pose.pose.orientation
        self.robot_pose = self.get_yaw_from_quaternion(orientation)

    def scan_callback(self, msg):
        scan_angle = [0, 30, 330]
        
        ranges = msg.ranges
        range_max = msg.range_max

        for num in range(3):
            angle_index = scan_angle[num]
            
            if angle_index < len(ranges):
                dist = ranges[angle_index]
                if math.isinf(dist) or math.isnan(dist):
                    self.scan_data[num] = range_max
                else:
                    self.scan_data[num] = dist

    def update_cmd_vel(self, linear, angular):
        cmd_vel = Twist()
        cmd_vel.linear.x = linear
        cmd_vel.angular.z = angular
        self.cmd_vel_pub.publish(cmd_vel)

    def update_callback(self):
        escape_range = 30.0 * DEG2RAD
        check_forward_dist = 0.7
        check_side_dist = 0.6

        if self.turtlebot3_state_num == GET_TB3_DIRECTION:
            if self.scan_data[CENTER] > check_forward_dist:
                if self.scan_data[LEFT] < check_side_dist:
                    self.prev_robot_pose = self.robot_pose
                    self.turtlebot3_state_num = TB3_RIGHT_TURN
                elif self.scan_data[RIGHT] < check_side_dist:
                    self.prev_robot_pose = self.robot_pose
                    self.turtlebot3_state_num = TB3_LEFT_TURN
                else:
                    self.turtlebot3_state_num = TB3_DRIVE_FORWARD
            
            if self.scan_data[CENTER] < check_forward_dist:
                self.prev_robot_pose = self.robot_pose
                self.turtlebot3_state_num = TB3_RIGHT_TURN

        elif self.turtlebot3_state_num == TB3_DRIVE_FORWARD:
            self.update_cmd_vel(LINEAR_VELOCITY, 0.0)
            self.turtlebot3_state_num = GET_TB3_DIRECTION

        elif self.turtlebot3_state_num == TB3_RIGHT_TURN:
            diff = abs(self.prev_robot_pose - self.robot_pose)
            
            if diff >= escape_range:
                self.turtlebot3_state_num = GET_TB3_DIRECTION
            else:
                self.update_cmd_vel(0.0, -1 * ANGULAR_VELOCITY)

        elif self.turtlebot3_state_num == TB3_LEFT_TURN:
            diff = abs(self.prev_robot_pose - self.robot_pose)
            
            if diff >= escape_range:
                self.turtlebot3_state_num = GET_TB3_DIRECTION
            else:
                self.update_cmd_vel(0.0, ANGULAR_VELOCITY)

        else:
            self.turtlebot3_state_num = GET_TB3_DIRECTION

def main(args=None):
    rclpy.init(args=args)
    turtlebot3_drive = Turtlebot3Drive()
    
    try:
        rclpy.spin(turtlebot3_drive)
    except KeyboardInterrupt:
        pass
    finally:
        turtlebot3_drive.update_cmd_vel(0.0, 0.0)
        turtlebot3_drive.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()