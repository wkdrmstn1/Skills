import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2
import numpy as np

class LidarProcessor(Node):
    def __init__(self):
        super().__init__('lidar_processor')

        # 3d 라이다 데이터 구독 
        self.subscription = self.create_subscription(
            PointCloud2,
            '/points',
            self.listener_callback,
            10
        )
 
        # 거리 필터링 이후의 결과값을 발행 
        self.publisher_ = self.create_publisher(
            PointCloud2,
            '/filtered_points',
            10
        )

    def listener_callback(self, msg):
    
        # 구조화된 리스트 형태로 점군을 읽어들이기 
        point_list = pc2.read_points_list(
            msg,
            field_names=("x", "y", "z"),
            skip_nans=True
        )
        
        # 넘파이 배열로 변환 파이 ㅂ
        points = np.array(point_list, dtype=np.float32)

        if points.size == 0:
            return

        # linalg : 선형대수 
        # norm 은 점과의 거리를 구해준다 (벡터값을 구해준다) 
        distances = np.linalg.norm(points, axis=1)
        filtered_points = points[distances <= 2.0] # 불린 인덱싱 

        # 필터링한 결과. 즉, 2m 안의 점들만 모아서 메시지로 만들고 토픽 발행 
        filtered_msg = pc2.create_cloud_xyz32(
            msg.header,
            filtered_points
        )

        self.publisher_.publish(filtered_msg)

        self.get_logger().info(
            f'Original: {len(points)} -> Filtered: {len(filtered_points)}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = LidarProcessor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
