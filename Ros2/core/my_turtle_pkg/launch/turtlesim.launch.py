# turtle_sim.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    # 1. Turtlesim 시뮬레이터
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='sim',
        output='screen'
    )

    # 2. 내가 만든 회전 노드
    # 내 노드는 /cmd_vel로 보내는데, Turtlesim은 /turtle1/cmd_vel을 듣습니다.
    # 따라서 remappings가 필요합니다!
    my_circle_node = Node(
        package='my_turtle_pkg',
        executable='circle_node',
        name='my_driver',
        output='screen',
        remappings=[('/cmd_vel', '/turtle1/cmd_vel')]
    )

    return LaunchDescription([
        turtlesim_node,
        my_circle_node
    ])