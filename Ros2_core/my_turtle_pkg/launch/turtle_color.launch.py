# turtle_color.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    # 파라미터를 주입한 Turtlesim 노드
    red_turtlesim = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='red_sim',
        output='screen',
        parameters=[
            {'background_r': 255}, # Red
            {'background_g': 0},   # Green
            {'background_b': 255}    # Blue
        ]
    )

    my_circle_node = Node(
        package='my_turtle_pkg',
        executable='circle_node',
        name='my_driver',
        output='screen',
        remappings=[('/cmd_vel', '/turtle1/cmd_vel')]
    )

    return LaunchDescription([
        red_turtlesim,
        my_circle_node
    ])