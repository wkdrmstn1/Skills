from setuptools import find_packages, setup

package_name = 'ros2_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jgs',
    maintainer_email='jgs@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'cv_bridge_cam = ros2_pkg.cv_bridge_cam:main',
            'cv_bridge_yolo = ros2_pkg.cv_bridge_yolo:main',
            'basic_drive = ros2_pkg.basic_drive:main',
            'turtlebot3_drive = ros2_pkg.turtlebot3_drive:main'
        ],
    },
)
