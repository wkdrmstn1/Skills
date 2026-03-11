import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # 파라미터가 작성된 파일의 경로 
    config_path = PathJoinSubstitution([
        FindPackageShare('my_param_pkg'), 'config', 'params.yaml'
    ])

    return LaunchDescription([
        Node(
            package='my_param_pkg',
            executable='param_node',
            name='custom_param_node', # YAML 파일의 노드명과 일치해야 함!
            output='screen',
            parameters=[config_path] # 파일 경로를 리스트에 넣음
        )
    ])