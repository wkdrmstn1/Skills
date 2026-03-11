import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor

class ParamNode(Node):
    def __init__(self):
        super().__init__('param_test_node')
        
        my_descriptor = ParameterDescriptor(description='abs', read_only=True)
        self.max_speed = 0.25
        
        self.declare_parameter('sensor_range', 3.5)
        self.declare_parameter('max_speed',0.25, descriptor=my_descriptor)
        self.declare_parameter('robot_color','blue')
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        current_speed = self.max_speed
        self.get_logger().info(f'max_speed :{current_speed}')
        

def main(args=None):
    rclpy.init(args=args)
    node = ParamNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()