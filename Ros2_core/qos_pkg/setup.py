from setuptools import find_packages, setup

package_name = 'qos_pkg'

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
            'qos_pub = qos_pkg.qos_pub:main',
            'qos_sub = qos_pkg.qos_sub:main',
            'qos_cv_pub = qos_pkg.qos_cv_pub:main',
            'qos_cv_sub = qos_pkg.qos_cv_sub:main'
        ],
    },
)
