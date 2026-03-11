from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_param_pkg',
            executable='param_node',
            name='custom_param_node',
            output='screen',
            # 딕셔너리 형태로 파라미터 주입
            parameters=[
                {'my_speed': 10.0},
                {'robot_name': 'SuperBot'}
            ]
        )
    ])