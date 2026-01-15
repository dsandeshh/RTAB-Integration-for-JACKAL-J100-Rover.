
#
# Example with gazebo:
#   1) Launch simulator (husky, nav2 and rtabmap):
#     $ ros2 launch rtabmap_demos jackal_sim_scan3d_demo.launch.py robot_ns:=j100_0029
#
#   2) Click on "Play" button on bottom-left of gazebo as soon as you can see it to avoid controllers crashing after 5 sec.
#
#   3) Move the robot:
#     b) By sending goals with RVIZ's "Nav2 Goal" button in action bar.
#     a) By teleoperating:
#        $ ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/a200_0000/cmd_vel
#

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

import os

ARGUMENTS = [
    DeclareLaunchArgument('rtabmap_viz', default_value='true',
                          choices=['true', 'false'], description='Start rtabmap_viz.'),
    DeclareLaunchArgument('localization', default_value='false',
                          choices=['true', 'false'], description='Start rtabmap in localization mode (a map should have been already created).'),
    DeclareLaunchArgument('world', default_value='warehouse',
                          description='Ignition World'),
    DeclareLaunchArgument('robot_ns', default_value='j100_0029',
                          description='Robot namespace'),
    DeclareLaunchArgument('use_camera', default_value='true',
                          description='Use camera for global loop closure / re-localization.'),
]

def generate_launch_description():
    # Directories
    pkg_clearpath_gz = get_package_share_directory(
        'clearpath_gz')
    pkg_clearpath_viz = get_package_share_directory(
        'clearpath_viz')
    pkg_rtabmap_demos = get_package_share_directory(
        'rtabmap_demos')
    pkg_clearpath_nav2_demos = get_package_share_directory(
        'clearpath_nav2_demos')
    
    # Paths
    sim_launch = PathJoinSubstitution(
        [pkg_clearpath_gz, 'launch', 'simulation.launch.py'])
    viz_launch = PathJoinSubstitution(
        [pkg_clearpath_viz, 'launch', 'view_navigation.launch.py'])
    rtabmap_launch = PathJoinSubstitution(
        [pkg_rtabmap_demos, 'launch', 'jackal', 'jackal_slam3d.launch.py'])
    nav2_launch = PathJoinSubstitution(
        [pkg_clearpath_nav2_demos, 'launch', 'nav2.launch.py'])

    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([sim_launch]),
        launch_arguments=[
            ('world', LaunchConfiguration('world')),
        ]
    )

    viz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([viz_launch]),
        launch_arguments=[
            ('namespace', LaunchConfiguration('robot_ns')),
        ]
    )

    rtabmap = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([rtabmap_launch]),
        launch_arguments=[
            ('rtabmap_viz', LaunchConfiguration('rtabmap_viz')),
            ('localization', LaunchConfiguration('localization')),
            ('use_sim_time', 'true'),
            ('use_camera', LaunchConfiguration('use_camera')),
            ('robot_ns', LaunchConfiguration('robot_ns'))
        ]
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([nav2_launch]),
        launch_arguments=[
            ('setup_path', os.path.expanduser('~')+'/clearpath/'),
            ('use_sim_time', 'true'),
        ]
    )

    # Create launch description and add actions
    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(rtabmap)
    ld.add_action(sim)
    ld.add_action(viz)
    ld.add_action(nav2)
    return ld
