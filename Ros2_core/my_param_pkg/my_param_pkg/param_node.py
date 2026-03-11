import rclpy
from rclpy.node import Node

class ParamNode(Node):
    def __init__(self):
        super().__init__('param_test_node')
        
        # my_speed 라는 파라미터를 선언하면서, 1.0으로 초기화!
        self.declare_parameter('my_speed', 1.0)
        self.declare_parameter('robot_name', 'turtle_A')

        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
    
        speed = self.get_parameter('my_speed').get_parameter_value().double_value
        name = self.get_parameter('robot_name').get_parameter_value().string_value
        
        self.get_logger().info(f'[{name}] 현재 속도 설정: {speed} m/s')

def main(args=None):
    rclpy.init(args=args)
    node = ParamNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()