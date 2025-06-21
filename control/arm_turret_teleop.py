#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import sys
import termios
import tty

class CustomTeleop(Node):
    def __init__(self):
        super().__init__('custom_teleop')

        self.arm_1_pub = self.create_publisher(Float64, '/arm_link_1_position', 10)
        self.arm_2_pub = self.create_publisher(Float64, '/arm_link_2_position', 10)
        self.turret_base_pub = self.create_publisher(Float64, '/turret_base_joint_position', 10)
        self.turret_pub = self.create_publisher(Float64, '/turret_joint_position', 10)

        self.arm_1_pos = 0.0
        self.arm_2_pos = 0.0
        self.turret_base_pos = 0.0
        self.turret_pos = 0.0

        print("Use keys to control joints:\n"
              "w/s: arm_1 up/down\n"
              "e/d: arm_2 up/down\n"
              "a/f: turret base left/right\n"
              "q/r: turret rotate left/right\n"
              "x: exit")

        self.run_teleop()

    def run_teleop(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)

        try:
            while True:
                key = sys.stdin.read(1)

                if key == 'w':
                    self.arm_1_pos += 0.1
                    self.arm_1_pub.publish(Float64(data=self.arm_1_pos))
                elif key == 's':
                    self.arm_1_pos -= 0.1
                    self.arm_1_pub.publish(Float64(data=self.arm_1_pos))
                elif key == 'e':
                    self.arm_2_pos += 0.1
                    self.arm_2_pub.publish(Float64(data=self.arm_2_pos))
                elif key == 'd':
                    self.arm_2_pos -= 0.1
                    self.arm_2_pub.publish(Float64(data=self.arm_2_pos))
                elif key == 'a':
                    self.turret_base_pos += 0.1
                    self.turret_base_pub.publish(Float64(data=self.turret_base_pos))
                elif key == 'f':
                    self.turret_base_pos -= 0.1
                    self.turret_base_pub.publish(Float64(data=self.turret_base_pos))
                elif key == 'q':
                    self.turret_pos += 0.1
                    self.turret_pub.publish(Float64(data=self.turret_pos))
                elif key == 'r':
                    self.turret_pos -= 0.1
                    self.turret_pub.publish(Float64(data=self.turret_pos))
                elif key == 'x':
                    print("Exiting teleop.")
                    break

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def main(args=None):
    rclpy.init(args=args)
    teleop = CustomTeleop()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
