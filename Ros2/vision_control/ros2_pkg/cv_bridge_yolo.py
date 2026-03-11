import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO

class YoloSubscriber(Node):
    def __init__(self):
        super().__init__('yolo_subscriber')

        self.subscription = self.create_subscription(
            Image,
            'cv_bridge',
            self.listener_callback,
            10)
    
        self.br = CvBridge()
        self.model = YOLO('yolov8n.pt') 
        
        self.get_logger().info("subscriber & YOLO on!")

    def listener_callback(self, data):
        try:
            current_frame = self.br.imgmsg_to_cv2(data, "bgr8")
        
            results = self.model(current_frame, stream=True, conf=0.7)
            annotated_frame = results[0].plot()

            cv2.imshow("YOLOv8 Detection", annotated_frame)
            cv2.waitKey(200) 
            
        except Exception as e:
            self.get_logger().error(f'이미지 처리 중 오류 발생: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = YoloSubscriber()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()