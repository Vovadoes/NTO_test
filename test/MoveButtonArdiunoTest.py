import serial
import rospy
from geometry_msgs.msg import Twist

from move_funs import forward, to_right

rospy.init_node('MoveButtonArdiunoTest')

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

vel = Twist()

if __name__ == '__main__':
    ser = serial.Serial(
        '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.4.1:1.0-port0', 9600,
        timeout=0.5
    )
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if line == '1':
                forward(0.5, vel, pub)
                to_right(90, vel, pub)
                ser.flush()
