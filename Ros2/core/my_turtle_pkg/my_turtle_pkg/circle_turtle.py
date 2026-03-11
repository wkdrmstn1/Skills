import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CircleTurtle(Node):
    def __init__(self):
        super().__init__('circle_turtle_node') 
        
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.get_logger().info('🐢 로봇 회전 노드가 시작되었습니다!')

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 0.5  
        msg.angular.z = 0.5 
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CircleTurtle()
    try:
        rclpy.spin(node) # 노드가 죽지 않고 계속 실행되도록 함
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()