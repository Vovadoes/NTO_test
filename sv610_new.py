import json
from time import sleep, time

import serial

import rospy

from std_msgs.msg import String
from std_msgs.msg import Int64

from Reader import Reader


rospy.init_node("SV610")

sv610 = serial.Serial()
sv610.baudrate = 9600
sv610.port = "/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-port0"
sv610.dtr = False
# sv610.timeout = 0.5
sv610.open()
sv610.flushInput()
sv610.reset_input_buffer()

pub_move = rospy.Publisher("move_key", String, queue_size=10)
pub_speed = rospy.Publisher("speed_movement", Int64, queue_size=10)

move_s = String()
speed_int64 = Int64()

interval = 0.001

reader = Reader(sv610)


def reading_data():
    global move_s
    global speed_int64
    read_data = reader.readline().decode("utf-8")
    print('read_data', '=', read_data)
    if read_data != '':
        try:
            dct = json.loads(read_data)
            print('dct', '=', dct)
            move_s = dct['move']
            speed_int64 = dct['speed']
            pub_move.publish(move_s)
            pub_speed.publish(speed_int64)
            return True
        except json.JSONDecodeError as e:
            print("JSON:", e, read_data)
            return False
        except KeyError as e:
            print("KeyError", e)
            return False
    return None

old_time = 0
flag = False

sv610.reset_input_buffer()
while not rospy.is_shutdown():
    print('read')
    reading_data()
    sleep(0.2)
    print('write')
    sv610.write((json.dumps({"camera": 123}) + '\n').encode("utf-8"))