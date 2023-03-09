import random

import rospy
import serial

ser = serial.Serial(
    '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.4.1:1.0-port0',
    9600,
)
ser.flush()

if __name__ == '__main__':
    while not rospy.is_shutdown():
        ser.write(random.randint(0, 90))
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print("line =", line)
        rospy.sleep(0.1)
