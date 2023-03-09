import rospy
import serial

from std_msgs.msg import Bool

rospy.init_node("button_node")

pub = rospy.Publisher("button_topic", Bool, queue_size=10)

b = Bool()
b.data = False

ser = serial.Serial(
    '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.4.1:1.0-port0',
    9600,
)
ser.flush()
pub.publish(b.data)

if __name__ == '__main__':
    while not rospy.is_shutdown():
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print("line =", line, b.data)
            if line == '1' and not b.data :
                b.data = True
                pub.publish(b)
            elif line == '0' and b.data:
                b.data = False
                pub.publish(b)
        rospy.sleep(0.1)
        # pub.publish(b.data)
        # b.data = not b.data
