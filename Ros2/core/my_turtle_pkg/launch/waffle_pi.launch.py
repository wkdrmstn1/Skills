import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():

    config_path = PathJoinSubstitution([
        FindPackageShare('my_param_pkg'), 'config', 'params.yaml'
    ])

    my_circle_node = Node(
        package='my_turtle_pkg',
        executable='circle_node_25',
        name='waffle_driver',
        namespace='jgs',
        output='screen'
    )

    param_node = Node(
        package='my_turtle_pkg',
        executable='param_node',
        name='custom_param_node', 
        output='screen',
        parameters=[config_path] 
    )

    return LaunchDescription([
        my_circle_node,
        param_node
    ])