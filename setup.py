from setuptools import setup
import os
from glob import glob

package_name = 'my_ddrobot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py') or []),  # Ensure no empty list
        (os.path.join('share', package_name, 'model'), glob('model/*') or []),  # Ensure no empty list
        (os.path.join('share', package_name, 'config'), glob('config/*') or [] if os.path.exists('config') else []),  # Ensure no empty list and check config directory
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mohan Chandra S S',
    maintainer_email='mohanc.btech23@rvu.edu.in',
    description='Teleop-controlled fire sprinkler AGV robot',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'arm_turret_teleop = my_ddrobot.arm_turret_teleop:main',
            'avoid = my_ddrobot.lidar_avoid_node:main',
        ],
    },
)
