import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2

class LidarSubscriber(Node):
    def __init__(self):
        super().__init__('lidar_subscriber')
        self.subscription = self.create_subscription(
            PointCloud2,
            '/points',  # Publisher와 토픽명이 일치해야 함
            self.listener_callback,
            10)

    def listener_callback(self, msg):
    
        gen = pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True)
        
        count = 0
        for p in gen:
            if count < 5:
                self.get_logger().info(f'Point[{count}]: x={p[0]:.2f}, y={p[1]:.2f}, z={p[2]:.2f}')
            count += 1
        
        self.get_logger().info(f'Total points received: {count}')

def main(args=None):
    rclpy.init(args=args)
    node = LidarSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()