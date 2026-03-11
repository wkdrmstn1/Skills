# gazebo

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge    


class QoS_cv_pub(Node):
    def __init__(self):
        super().__init__('QoS_cv_pub')

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT, # 신뢰성: Best Effort
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.subscription = self.create_subscription(
            Image, 
            '/camera/image_raw',
            self.listener_callback, 
            qos_profile
        )

        self.publisher = self.create_publisher(
            Image,
            '/relayed_image',
            qos_profile)
        
        self.bridge = CvBridge()
        self.get_logger().info('waiting GAZEBO')

    def listener_callback(self,msg):

        self.publisher.publish(msg)
        self.get_logger().info('Publishing')



def main(args=None):
    rclpy.init(args=args)
    node = QoS_cv_pub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()