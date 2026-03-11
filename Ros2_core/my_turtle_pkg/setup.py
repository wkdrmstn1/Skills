from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_turtle_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
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
            'circle_node = my_turtle_pkg.circle_turtle:main',
            're_circle_node = my_turtle_pkg.re_circle_turtle:main',
            'circle_node_25 = my_turtle_pkg.circle_turtle_25:main',
            'param_node = my_turtle_pkg.param_node:main'
        ],
    },
)
