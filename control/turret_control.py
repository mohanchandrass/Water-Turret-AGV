#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class TurretControl(Node):
    def __init__(self):
        super().__init__('turret_control')
        self.publisher_ = self.create_publisher(Float64, '/turret_joint/command', 10)

    def control_turret(self, angle):
        msg = Float64()
        msg.data = angle  # Set angle in radians
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    turret_control = TurretControl()

    # Example: Rotate turret to 1.0 rad (about 57.3 degrees)
    turret_control.control_turret(1.0)

    rclpy.spin(turret_control)

if __name__ == '__main__':
    main()
