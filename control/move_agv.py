#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from pynput import keyboard

class MoveAGV(Node):
    def __init__(self):
        super().__init__('move_agv')

        # Publishers for controlling the AGV robot
        self.car_control_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.turret_control_pub = self.create_publisher(Float64, 'turret_angle', 10)
        self.nozzle_control_pub = self.create_publisher(Float64, 'nozzle_angle', 10)
        self.arm_link_1_pub = self.create_publisher(Float64, 'arm_link_1_angle', 10)
        self.arm_link_2_pub = self.create_publisher(Float64, 'arm_link_2_angle', 10)

        # Initialize variables for controlling movement
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        self.turret_angle = 0.0
        self.nozzle_angle = 0.0
        self.arm_link_1_angle = 0.0
        self.arm_link_2_angle = 0.0

        # Start listening for key presses
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

        # Timer to regularly publish control messages
        self.timer = self.create_timer(0.1, self.timer_callback)

    def on_key_press(self, key):
        try:
            if key.char == 'w':  # Move forward
                self.linear_velocity += 0.1
            elif key.char == 's':  # Move backward
                self.linear_velocity -= 0.1
            elif key.char == 'a':  # Turn left
                self.angular_velocity += 0.1
            elif key.char == 'd':  # Turn right
                self.angular_velocity -= 0.1
            elif key.char == 'q':  # Rotate turret counterclockwise
                self.turret_angle += 5.0
            elif key.char == 'e':  # Rotate turret clockwise
                self.turret_angle -= 5.0
            elif key.char == 'r':  # Tilt nozzle up
                self.nozzle_angle += 5.0
            elif key.char == 'f':  # Tilt nozzle down
                self.nozzle_angle -= 5.0
            elif key.char == 't':  # Move arm link 1 up
                self.arm_link_1_angle += 5.0
            elif key.char == 'g':  # Move arm link 1 down
                self.arm_link_1_angle -= 5.0
            elif key.char == 'y':  # Move arm link 2 up
                self.arm_link_2_angle += 5.0
            elif key.char == 'h':  # Move arm link 2 down
                self.arm_link_2_angle -= 5.0
            elif key.char == 'x':  # Stop all movement
                self.linear_velocity = 0.0
                self.angular_velocity = 0.0
                self.turret_angle = 0.0
                self.nozzle_angle = 0.0
                self.arm_link_1_angle = 0.0
                self.arm_link_2_angle = 0.0
        except AttributeError:
            pass

    def timer_callback(self):
        # Create messages to send to each controller
        twist = Twist()
        twist.linear.x = self.linear_velocity
        twist.angular.z = self.angular_velocity
        self.car_control_pub.publish(twist)

        turret_msg = Float64()
        turret_msg.data = self.turret_angle
        self.turret_control_pub.publish(turret_msg)

        nozzle_msg = Float64()
        nozzle_msg.data = self.nozzle_angle
        self.nozzle_control_pub.publish(nozzle_msg)

        arm_link_1_msg = Float64()
        arm_link_1_msg.data = self.arm_link_1_angle
        self.arm_link_1_pub.publish(arm_link_1_msg)

        arm_link_2_msg = Float64()
        arm_link_2_msg.data = self.arm_link_2_angle
        self.arm_link_2_pub.publish(arm_link_2_msg)

def main(args=None):
    rclpy.init(args=args)
    move_agv = MoveAGV()

    rclpy.spin(move_agv)

    move_agv.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
