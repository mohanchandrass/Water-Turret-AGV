import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # Define package and file paths
    package_name = 'my_ddrobot'
    robot_xacro_path = 'model/my_dd_robot_model.xacro'
    
    # Get robot description (URDF) from the xacro file
    robot_description_path = os.path.join(get_package_share_directory(package_name), robot_xacro_path)
    robot_description = xacro.process_file(robot_description_path).toxml()

    # Define the robot state publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
    )

    # Define the RViz node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', os.path.join(get_package_share_directory(package_name), 'config', 'my_dd_robot.rviz')]
    )

    # Return the launch description with the necessary nodes
    return LaunchDescription([
        robot_state_publisher,
        rviz_node
    ])
