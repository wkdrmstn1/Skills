from setuptools import find_packages, setup

package_name = '3d_pkg'

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
    maintainer_email='geunsu356@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'pub=3d_pkg.pub:main',
            'sub=3d_pkg.sub:main',
            'test=3d_pkg.test:main'
        ],
    },
)
