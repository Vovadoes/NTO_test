import json
from time import sleep, time

import serial

import rospy
from random import randint

from std_msgs.msg import String
from std_msgs.msg import Int64
from std_msgs.msg import Bool

from Reader import Reader
from cam import get_data

# rospy.init_node("SV610")

sv610 = serial.Serial()
sv610.baudrate = 57600
sv610.port = "/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-port0"
sv610.dtr = False
# sv610.timeout = 0.5
sv610.open()
sv610.flushInput()
sv610.reset_input_buffer()

print(serial.__version__)

pub_move = rospy.Publisher("rotate", Int64, queue_size=10)
pub_speed = rospy.Publisher("distance", Int64, queue_size=10)
pub_hc12 = rospy.Publisher("HC12Value", Bool, queue_size=10)
pub_servo = rospy.Publisher("servo", Int64, queue_size=10)
pub_id_data = rospy.Publisher("id_data", Int64, queue_size=10)

rotate = String()
distance = Int64()
hc12_value = Bool()
servo = Int64()
id_data = Int64()

reader = Reader(sv610, max_delay=0.5)


def reading_data():
    global rotate
    global distance

    read_data = reader.readline()
    print('read_data', '=', read_data)
    read_data = read_data.decode("utf-8")
    print('read_data', '=', read_data)
    if read_data != '':
        try:
            dct = json.loads(read_data)
            print('dct', '=', dct)
            rotate.data = dct['move']
            distance.data = dct['speed']

            pub_move.publish(rotate)
            pub_speed.publish(distance)

            hc12_value.data = dct['hc12']
            pub_hc12.publish(hc12_value)

            servo.data = dct['servo']
            pub_servo.publish(servo)

            id_data.data = dct['id']
            pub_servo.publish(id_data)

            return True
        except json.JSONDecodeError as e:
            print("JSON:", e, read_data)
            return False
        except KeyError as e:
            print("KeyError", e)
            return False
    return None


sv610.reset_input_buffer()
while not rospy.is_shutdown():
    time_old = time()
    print('reading')
    reading_data()
    print('end reading: ', (time() - time_old) * 1000)
    time_old = time()
    print('write')
    #sv610.write(get_data() + b'\t\n\t\n')
    sv610.write(b'\xad\xdd\x06\x24\x01\x07\x07\x07\x02\x01\x01\x00\x00\x00\x00\x00\x00' + b'\t\n\t\n')
    print('end writing: ', (time() - time_old) * 1000)