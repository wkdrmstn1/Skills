import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class QoS_pub(Node):
    def __init__(self):
        super().__init__('QoS_pub')

        my_qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT, # 신뢰성: Best Effort
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.publisher_ = self.create_publisher(
            String, 
            'sensor_data', 
            qos_profile=my_qos_profile # 여기에 적용!
        )

        self.timer = self.create_timer(3, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'QoS test'

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing')

        # 1~3초 간격으로 위 토픽을 발행하면 됩니다.

def main(args=None):
    rclpy.init(args=args)
    node = QoS_pub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # 종료 시 정지
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()