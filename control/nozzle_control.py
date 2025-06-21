#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class NozzleControl(Node):
    def __init__(self):
        super().__init__('nozzle_control')
        self.publisher_ = self.create_publisher(Float64, '/nozzle/command', 10)

    def control_nozzle(self, pressure):
        msg = Float64()
        msg.data = pressure  # Nozzle pressure value (arbitrary units)
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    nozzle_control = NozzleControl()

    # Example: Set nozzle pressure to 0.8
    nozzle_control.control_nozzle(0.8)

    rclpy.spin(nozzle_control)

if __name__ == '__main__':
    main()
