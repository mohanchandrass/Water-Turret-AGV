#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import sys
import termios
import tty
import select

class ArmTeleopNode(Node):
    def __init__(self):
        super().__init__('arm_teleop_control')

        self.arm1_pub = self.create_publisher(Float64, '/arm_link_1_position', 10)
        self.arm2_pub = self.create_publisher(Float64, '/arm_link_2_position', 10)
        self.turret_pub = self.create_publisher(Float64, '/turret_joint_position', 10)

        self.arm1_pos = 0.0
        self.arm2_pos = 0.0
        self.turret_pos = 0.0
        self.step = 0.1

        self.settings = termios.tcgetattr(sys.stdin)

        self.get_logger().info("Control your fire sprinkler arm!\n"
                               "q/w : arm_link_1 down/up\n"
                               "a/s : arm_link_2 down/up\n"
                               "z/x : turret left/right\n"
                               "CTRL-C to quit")

        self.run()

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        key = ''
        if rlist:
            key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def run(self):
        try:
            while rclpy.ok():
                key = self.getKey()
                if key == 'q':
                    self.arm1_pos += self.step
                elif key == 'w':
                    self.arm1_pos -= self.step
                elif key == 'a':
                    self.arm2_pos += self.step
                elif key == 's':
                    self.arm2_pos -= self.step
                elif key == 'z':
                    self.turret_pos += self.step
                elif key == 'x':
                    self.turret_pos -= self.step
                elif key == '\x03':  # Ctrl-C
                    break

                self.arm1_pub.publish(Float64(data=self.arm1_pos))
                self.arm2_pub.publish(Float64(data=self.arm2_pos))
                self.turret_pub.publish(Float64(data=self.turret_pos))
        except Exception as e:
            self.get_logger().error(f"Exception: {e}")
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

def main(args=None):
    rclpy.init(args=args)
    node = ArmTeleopNode()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
