# gazebo

import rclpy
import cv2 
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge    


class QoS_cv_sub(Node):
    def __init__(self):
        super().__init__('QoS_cv_sub')

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT, # 신뢰성: Best Effort
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.subscription = self.create_subscription(
            Image, 
            '/relayed_image',
            self.listener_callback, 
            qos_profile
        )
    
        self.bridge = CvBridge()
        self.get_logger().info('Subscribing')

    def listener_callback(self,msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
            cv2.imshow('GAZEBO',cv_image)
            cv2.waitKey(1)

        except Exception as e:
            self.get_logger().error(e)


def main(args=None):
    rclpy.init(args=args)
    node = QoS_cv_sub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()