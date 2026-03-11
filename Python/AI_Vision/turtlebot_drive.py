import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, qos_profile_sensor_data

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

from transforms3d.euler import quat2euler


DEG2RAD = math.pi / 180.0

LINEAR_VELOCITY = 0.15
ANGULAR_VELOCITY = 0.5

CENTER = 0
LEFT = 1
RIGHT = 2

GET_TB3_DIRECTION = 0
TB3_DRIVE_FORWARD = 1
TB3_RIGHT_TURN = 2
TB3_LEFT_TURN = 3


class Turtlebot3Drive(Node):

    def __init__(self):
        super().__init__('my_drive')

        self.scan_data = [0.0, 0.0, 0.0]
        self.robot_pose = 0.0
        self.prev_robot_pose = 0.0

        self.turtlebot3_state_num = GET_TB3_DIRECTION

        qos = QoSProfile(depth=10)

        self.cmd_vel_pub = self.create_publisher(
            Twist,
            'cmd_vel',
            qos
        )

        self.scan_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            qos_profile_sensor_data
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            'odom',
            self.odom_callback,
            qos
        )

        self.update_timer = self.create_timer(
            0.01,
            self.update_callback
        )

        self.get_logger().info('Turtlebot3 simulation node has been initialised')

    def destroy_node(self):
        self.get_logger().info('Turtlebot3 simulation node has been terminated')
        super().destroy_node()

    def odom_callback(self, msg: Odometry):
        orientation_q = msg.pose.pose.orientation
        quaternion = (
            orientation_q.x,
            orientation_q.y,
            orientation_q.z,
            orientation_q.w
        )
        _, _, yaw = quat2euler(quaternion)
        self.robot_pose = yaw

    def scan_callback(self, msg: LaserScan):
        scan_angle = [0, 30, 330]

        for i in range(3):
            distance = msg.ranges[scan_angle[i]]
            if math.isinf(distance):
                self.scan_data[i] = msg.range_max
            else:
                self.scan_data[i] = distance

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
            if abs(self.prev_robot_pose - self.robot_pose) >= escape_range:
                self.turtlebot3_state_num = GET_TB3_DIRECTION
            else:
                self.update_cmd_vel(0.0, -ANGULAR_VELOCITY)

        elif self.turtlebot3_state_num == TB3_LEFT_TURN:
            if abs(self.prev_robot_pose - self.robot_pose) >= escape_range:
                self.turtlebot3_state_num = GET_TB3_DIRECTION
            else:
                self.update_cmd_vel(0.0, ANGULAR_VELOCITY)

        else:
            self.turtlebot3_state_num = GET_TB3_DIRECTION


def main(args=None):
    rclpy.init(args=args)
    node = Turtlebot3Drive()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
