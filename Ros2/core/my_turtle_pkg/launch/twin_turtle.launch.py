# turtle_color.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    # 파라미터를 주입한 Turtlesim 노드
    room1 = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='room1',
        output='screen'
    )

    room2 = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='room2',
        output='screen',
        parameters=[
            {'background_r': 255}, # Red
            {'background_g': 255},   # Green
            {'background_b': 0}    # Blue
        ],
        remappings=[('/turtle1/cmd_vel', '/room2/cmd_vel')]     # N번째 거북이 또한 turtle1
    )
    room3 = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='room3',
        output='screen',
        parameters=[
            {'background_r': 255}, # Red
            {'background_g': 0},   # Green
            {'background_b': 255}    # Blue
        ],
        remappings=[('/turtle1/cmd_vel', '/room3/cmd_vel')]     # N번째 거북이 또한 turtle1
    )

    my_circle_node = Node(
        package='my_turtle_pkg',
        executable='circle_node',
        name='circle',
        output='screen',
        remappings=[('/cmd_vel', '/room2/cmd_vel')]
    )
    re_my_circle_node = Node(
        package='my_turtle_pkg',
        executable='re_circle_node',
        name='re_circle',
        output='screen',
        remappings=[('/cmd_vel', '/room3/cmd_vel')]
    )

    return LaunchDescription([
        room1,
        room2,
        room3,
        my_circle_node,
        re_my_circle_node
    ])




'''
# twin_turtles.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    turtlesim_room1 = Node(
        package='turtlesim',
        executable='turtlesim_node',
        namespace='room1',
        name='room1',
        output='screen'
    )

    turtlesim_room2 = Node(
        package='turtlesim',
        executable='turtlesim_node',
        namespace='room2',
        output='screen',
        parameters=[
            {'background_r': 255}, 
            {'background_g': 255},  
            {'background_b': 0}  
        ]
    )

    my_circle_node = Node(
        package='my_turtle_pkg',
        executable='circle_node',
        name='my_driver',
        output='screen',
        remappings=[('/cmd_vel', '/room2/turtle1/cmd_vel')]
    )

    return LaunchDescription([
        turtlesim_room1,
        turtlesim_room2,
        my_circle_node
    ])
'''