#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from pynput import keyboard

class TeleopArmLink2(Node):
    def __init__(self):
        super().__init__('teleop_arm_link_2')
        self.publisher = self.create_publisher(Float64, '/arm_link_2/command', 10)
        self.angle = 0.0  # Start at the initial position

        # Set up the listener for the keyboard
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            if key.char == 'c':  # Move arm link 2 in one direction (increase angle)
                self.angle += 0.1  # Increment angle
            elif key.char == 'v':  # Move arm link 2 in the opposite direction (decrease angle)
                self.angle -= 0.1  # Decrement angle

            # Keep the angle within a reasonable range (optional, depending on the robot)
            self.angle = max(min(self.angle, 1.5), -1.5)

            # Publish the angle to the arm link 2
            self.publisher.publish(Float64(self.angle))

        except AttributeError:
            pass  # Handle special keys

def main():
    rclpy.init()
    teleop_arm_link_2 = TeleopArmLink2()
    rclpy.spin(teleop_arm_link_2)
    teleop_arm_link_2.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
