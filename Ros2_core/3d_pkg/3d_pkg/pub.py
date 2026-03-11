import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
import sensor_msgs_py.point_cloud2 as pc2
import numpy as np

class DummyLidarPublisher(Node):
    def __init__(self):
        super().__init__('dummy_lidar_publisher')
        
        # /points 는 일반적인 3d 라이다 토픽의 명칭 
        self.publisher_ = self.create_publisher(PointCloud2, '/points', 10)
        self.timer = self.create_timer(0.1, self.timer_callback) # 10hz

    def timer_callback(self):
    
        # 센서 데이터의 메타 데이터를 담당하는 헤더 
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = 'lidar_frame'

        num_points = 100 # 가상의 점을 100개 정도 해보자 
        
        # 100개의 점은 각 3개의 차원을 가진다 
        points = np.random.rand(num_points, 3).astype(np.float32)
        
        # 스케일링 (범위를 조정한다) : -5 ~ 5 사이 
        points = (points * 10) - 5 
        
        # 점군 생성 (토픽 메시지 형태로) 
        pc_msg = pc2.create_cloud_xyz32(header, points)

        self.publisher_.publish(pc_msg)
        self.get_logger().info(f'Publishing {num_points} dummy points')

def main(args=None):
    rclpy.init(args=args)
    node = DummyLidarPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()