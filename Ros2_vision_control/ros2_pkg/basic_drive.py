import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
import numpy as np

class TurtlebotController(Node):
    def __init__(self):
        super().__init__('turtlebot_controller')
        
        # 1. QoS 설정 (렉 방지용 Best Effort)
        qos_policy = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            depth=10
        )

        # 2. Publisher (명령 보내기)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 3. Subscriber (라이다 받기)
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            qos_policy)

        # 4. 타이머 (0.05초마다 명령 전송 - Heartbeat)
        self.timer = self.create_timer(0.05, self.timer_callback)

        self.linear_x = 0.0
        self.angular_z = 0.0
        self.get_logger().info("start")

    def listener_callback(self, msg):
        # 데이터 처리
        ranges = np.array(msg.ranges)
        ranges = np.nan_to_num(ranges, posinf=10.0, neginf=0.0, nan=10.0)

        # 360도 데이터 분할
        f = np.min(np.concatenate([ranges[:20], ranges[-20:]]))
        l = np.min(ranges[60:120])
        r = np.min(ranges[240:300])

        # 주행 로직
        if f <= 0.6:
            self.linear_x = -0.5
            self.angular_z = 0.0
            if l > r:
                self.linear_x = 0.0
                self.angular_z = 0.5  # 좌회전
            else:
                self.linear_x = 0.0
                self.angular_z = -0.5 # 우회전
        else:
            self.linear_x = 0.2  # 전진
            self.angular_z = 0.0

    def timer_callback(self):
        # 결정된 명령을 로봇에게 전송
        msg = Twist()
        msg.linear.x = self.linear_x
        msg.angular.z = self.angular_z
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TurtlebotController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # 종료 시 정지
        stop_msg = Twist()
        node.publisher_.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()