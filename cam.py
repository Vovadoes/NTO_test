from __future__ import print_function

import sys

from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
import rospy
import pprint
import imageio.v3 as iio
import numpy as np
from PIL import Image
import cv2


data = b''
# def translation_img(webm_bytes: bytes):  # file: bytes
#     src = iio.imread(webm_bytes).astype('float32')
#     print('Размер до =', sys.getsizeof(src))
#     scale_percent = 25
#     width = int(src.shape[1] * scale_percent / 100)
#     height = int(src.shape[0] * scale_percent / 100)
#     dsize = (width, height)
#     output = cv2.resize(src, dsize)
#     print('Размер после =', sys.getsizeof(output))
#     return output.tobytes()
def get_data():
    with open("files/my_file_test.txt", "wb") as binary_file:
        # Write bytes to file
        binary_file.write(data)
    pprint.pprint(data)
    return data

def callback(msg):
    global data
    data =  msg.data


# def take_photo(msg):
#     list_res = list(map(int, msg.data.split(';')[:-1]))
#
#     frames = np.resize(np.array(list_res, dtype=int), (480, 640, 3))
#     img_float32 = np.float32(frames)
#     color_image_rgb = cv2.cvtColor(img_float32, cv2.COLOR_BGR2RGB)
#     cv2.imwrite('waka.jpg', color_image_rgb)


rospy.init_node('SV610')
rospy.Subscriber("front_camera/image_raw/compressed", CompressedImage, callback)  # получаем данные
# rospy.Subscriber("image/photo", String, take_photo)
