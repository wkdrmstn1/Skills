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

    # FindPackageShare : 런치파일 관련 내용이 포함된 share 폴더에서 특정 패키지 경로 찾기 
    pkg_gazebo_ros = FindPackageShare(package='turtlebot3_gazebo').find('turtlebot3_gazebo')

	# 가제보 패키지를 찾았으니, 그 안에 있는 런치파일을 포함해서 이 런치파일을 실행하겠다
    start_gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'turtlebot3_world.launch.py')
        )
    )

    my_circle_node = Node(
        package='my_turtle_pkg',
        executable='circle_node_25',
        namespace = 'jgs',
        name='waffle_driver',
        output='screen',
        remappings=[
            ('/turtle1/cmd_vel', '/cmd_vel')]
    )
    param_node = Node(
            package='my_turtle_pkg',
            executable='param_node',
            name='custom_param_node', # YAML 파일의 노드명과 일치해야 함!
            output='screen',
            parameters=[config_path] # 파일 경로를 리스트에 넣음
        )

    return LaunchDescription([
        start_gazebo_cmd,
        my_circle_node,
        param_node
    ])