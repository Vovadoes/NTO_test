import rospy
import serial

from std_msgs.msg import Int64
from std_msgs.msg import Bool

from Mover import RobotMover

rospy.init_node('Management')
rotate = ''
distance = 0
hc12_value = False
id_pushed = -1
id_data = 0
servo_rotate = 0


def rotate_callback(msg):
    global rotate
    global flag
    flag = False
    rotate = msg.data


def distance_callback(msg):
    global distance
    distance = msg.data


def HC12_callback(msg):
    global hc12_value
    hc12_value = msg.data


def id_callback(msg):
    global id_data
    id_data = msg.data

def servo_callback(msg):
    global servo_rotate
    servo_rotate = msg.data

rospy.Subscriber("rotate", Int64, rotate_callback)
rospy.Subscriber("distance", Int64, distance_callback)
rospy.Subscriber("HC12Value", Bool, HC12_callback)
rospy.Subscriber("id_data", Int64, id_callback)
rospy.Subscriber("servo", Int64, servo_callback)

ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.4.1:1.0-port0', 9600, timeout=1)
ser.flush()

mover = RobotMover(init_node=True)
while not rospy.is_shutdown():
    rospy.sleep(0.1)
    if id_pushed != id_data:
        id_pushed = id_data
        if rotate != 0:
            mover.to_right(rotate)
        if distance != 0:
            mover.forward(distance)
        ser.write(servo_rotate)


rospy.spin()
