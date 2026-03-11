import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class QoS_sub(Node):
    def __init__(self):
        super().__init__('Qos_sub')

        my_qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT, # 신뢰성: Best Effort
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.subscripton = self.create_subscription(
            String, 
            'sensor_data', 
            self.listener_callback,
            qos_profile=my_qos_profile # 여기에 적용!
        )

    def listener_callback(self,msg):
        self.get_logger().info(msg.data)



def main(args=None):
    rclpy.init(args=args)
    node = QoS_sub()
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