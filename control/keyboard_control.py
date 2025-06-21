#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from pynput import keyboard

class KeyboardControl(Node):
    def __init__(self):
        super().__init__('keyboard_control')

        # Publisher for controlling car
        self.car_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Publisher for turret
        self.turret_pub = self.create_publisher(Float64, '/turret_joint/command', 10)

        # Publishers for arm links
        self.arm_link_1_pub = self.create_publisher(Float64, '/arm_joint_1/command', 10)
        self.arm_link_2_pub = self.create_publisher(Float64, '/arm_joint_2/command', 10)

        # Publisher for nozzle control
        self.nozzle_pub = self.create_publisher(Float64, '/nozzle/command', 10)

        # Initialize variables
        self.car_msg = Twist()
        self.turret_msg = Float64()
        self.arm_link_1_msg = Float64()
        self.arm_link_2_msg = Float64()
        self.nozzle_msg = Float64()

        # Listen to keyboard events
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            if key.char == 'w':  # Move forward
                self.car_msg.linear.x = 1.0
            elif key.char == 's':  # Move backward
                self.car_msg.linear.x = -1.0
            elif key.char == 'a':  # Turn left
                self.car_msg.angular.z = 1.0
            elif key.char == 'd':  # Turn right
                self.car_msg.angular.z = -1.0
            elif key.char == 'f':  # Spray water (nozzle)
                self.nozzle_msg.data = 1.0  # Example pressure value
            elif key.char == 'z':  # Stop spray
                self.nozzle_msg.data = 0.0
            elif key.char == 'x':  # Control arm link 1 (rotate)
                self.arm_link_1_msg.data += 0.1  # Increment angle
            elif key.char == 'c':  # Control arm link 2 (rotate)
                self.arm_link_2_msg.data += 0.1  # Increment angle
            elif key == keyboard.Key.left:  # Turn turret left
                self.turret_msg.data += 0.1
            elif key == keyboard.Key.right:  # Turn turret right
                self.turret_msg.data -= 0.1

        except AttributeError:
            pass

        # Publish the messages
        self.car_pub.publish(self.car_msg)
        self.turret_pub.publish(self.turret_msg)
        self.arm_link_1_pub.publish(self.arm_link_1_msg)
        self.arm_link_2_pub.publish(self.arm_link_2_msg)
        self.nozzle_pub.publish(self.nozzle_msg)

def main(args=None):
    rclpy.init(args=args)
    keyboard_control = KeyboardControl()
    rclpy.spin(keyboard_control)

if __name__ == '__main__':
    main()
