from __future__ import print_function

import roslib
import sys
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image, CompressedImage
from std_msgs.msg import String
from std_msgs.msg import Bool
import imageio.v3 as iio
from Mover import RobotMover

angular_speed = 0.4


# класс для обработки изображения
class BallProcessing:
    def __init__(self):
        # red hsv: (0, 50, 50), (15, 255, 255)
        # red rgb: (220, 20, 60), (139, 0, 0)
        # self.yellowLower = (60, 20, 220)  # dark
        # self.yellowUpper = (0, 0, 139)  # light
        self.yellowLower = (14, 180, 200)  # dark
        self.yellowUpper = (34, 255, 255)  # light

        self.x_value = 640  # длина
        self.y_value = 480  # ширина
        self.focus = 672.5  # фокусное расстояние 145

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (30, 50)
        self.fontScale = 0.5
        self.fontColor = (255, 255, 255)
        self.lineType = 1
        self.current_data = []

    def process(self, frame):
        # resize the frame, blur it, and convert it to the HSV
        # color space
        # frame = imutils.resize(frame, width=600)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.yellowLower, self.yellowUpper)

        # cv2.imshow("Frame2", mask)
        mask = cv2.erode(mask, None, iterations=2)  # эрозия
        mask = cv2.dilate(mask, None, iterations=2)  # расширение для удаления шума?

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        self.current_data = []
        # only proceed if at least one contour was found
        cv2.imwrite('test_2.jpg', frame)
        all_balls = []
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)  # x, y = центр?
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 3:
                # находим угол
                coef = 45 / (self.x_value // 2)  # сколько градусов в одном пикселе
                angle = (int(x) - (self.x_value // 2)) * coef
                # находим расстояние
                y_value = [i[0][0] for i in c]  # все y
                min_y = min(y_value)
                max_y = max(y_value)
                sh = max_y - min_y
                d_circle = 70  # мм
                distance = d_circle * self.focus / sh  # дистанция
                all_balls.append({"obj_x": int(x), "obj_y": int(y),
                                  "obj_r": int(radius), "obj_dist": distance,
                                  "obj_angle": angle})
        self.current_data: list = all_balls

    def get_current_data(self) -> list:
        return self.current_data


bp = BallProcessing()


# главный класс издателя и подписчика
class RecognitionImage:
    def __init__(self):
        self.img = None
        self.angle = None
        self.dist = None
        self.params = None
        # self.vel = Twist()
        self.img_details = rospy.Publisher("image/details", String,
                                           queue_size=1)  # сохранение данных
        rospy.Subscriber("front_camera/image_raw/compressed", CompressedImage,
                         self.callback_handler)  # получаем данные
        rospy.Subscriber("button_topic", Bool,
                         self.button_fun)  # получаем данные
        # self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.mover = RobotMover(init_node=True)
        self.flag = False
        self.button = False

    def button_fun(self, msg):
        if not self.button:
            self.button = msg.data

    def callback_handler(self, msg):
        self.img = iio.imread(msg.data)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

    def vel_publisher(self, value):  # Какие данные
        if not value:
            pass
        else:
            bp.process(self.img)  # frame - ред фото, которое можно выводить
            # cv2.imshow('frame', frame)  # показ камеры
            params: list = bp.get_current_data()  # берем полученные данные о шаре
            self.params = params
            if self.button:
                if not self.flag:
                    self.params.sort(key=lambda x: x["obj_dist"])
                    if len(self.params) == 0:
                        self.mover.to_left(10)
                        return
                    point = self.params[0]
                    self.flag = True
                else:
                    self.params = [i for i in self.params if self.params[i]["obj_angle"] < 0]
                    self.params.sort(key=lambda x: x["obj_dist"])
                    if len(self.params) == 0:
                        self.mover.to_left(10)
                        return
                    point = self.params[0]
                    self.flag = True
                if point["obj_angle"] >= 0:
                    self.mover.to_right(abs(point["obj_angle"]))
                else:
                    self.mover.to_left(abs(point["obj_angle"]))
                self.mover.forward(point["obj_dist"])
                self.button = False

    def save_info(self):
        if self.img is not None:  # если камера не работатет
            self.vel_publisher(True)
        else:
            self.vel_publisher(False)


if __name__ == '__main__':
    rospy.init_node('img_details')
    r = RecognitionImage()
    while not rospy.is_shutdown():
        rospy.sleep(0.5)
        r.save_info()

    rospy.spin()
