#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class ArmControl(Node):
    def __init__(self):
        super().__init__('arm_control')
        self.publisher_1 = self.create_publisher(Float64, '/arm_joint_1/command', 10)
        self.publisher_2 = self.create_publisher(Float64, '/arm_joint_2/command', 10)

    def control_arm(self, joint_1_angle, joint_2_angle):
        msg_1 = Float64()
        msg_1.data = joint_1_angle  # Joint 1 angle in radians

        msg_2 = Float64()
        msg_2.data = joint_2_angle  # Joint 2 angle in radians

        self.publisher_1.publish(msg_1)
        self.publisher_2.publish(msg_2)

def main(args=None):
    rclpy.init(args=args)
    arm_control = ArmControl()

    # Example: Move arm joints to certain angles (in radians)
    arm_control.control_arm(0.5, 1.2)

    rclpy.spin(arm_control)

if __name__ == '__main__':
    main()
