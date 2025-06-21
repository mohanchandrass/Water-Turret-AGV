import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro
from launch.substitutions import Command

def generate_launch_description():
    robot_name = 'my_dd_robot'
    pkg_name = 'my_ddrobot'

    urdf_path = os.path.join(get_package_share_directory(pkg_name), 'model', 'my_dd_robot_model.xacro')
    world_path = os.path.join(get_package_share_directory(pkg_name), 'worlds', 'maze.world')
    controllers_yaml = os.path.join(get_package_share_directory(pkg_name), 'config', 'controllers.yaml')

    robot_description = {'robot_description': Command(['xacro ', urdf_path])}

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world_path}.items()
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gzclient.launch.py')
        )
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', robot_name, '-topic', 'robot_description'],
        output='screen'
    )

    ros2_control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[robot_description, controllers_yaml],
        output='screen'
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen'
    )
    turret_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['turret_controller'],
        output='screen'
    )
    arm1_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['arm1_controller'],
        output='screen'
    )
    arm2_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['arm2_controller'],
        output='screen'
    )

    return LaunchDescription([
        gazebo_server,
        gazebo_client,
        robot_state_publisher_node,
        joint_state_publisher_node,
        spawn_entity_node,
        ros2_control_node,
        joint_state_broadcaster_spawner,
        turret_controller_spawner,
        arm1_controller_spawner,
        arm2_controller_spawner,
    ])
