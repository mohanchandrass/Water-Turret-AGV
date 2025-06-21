#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CarControl(Node):
    def __init__(self):
        super().__init__('car_control')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

    def send_velocity(self, linear_x, angular_z):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    car_control = CarControl()

    # Example: Move forward at 1 m/s, rotate at 0.5 rad/s
    car_control.send_velocity(1.0, 0.5)

    rclpy.spin(car_control)

if __name__ == '__main__':
    main()
