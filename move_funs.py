import rospy
from functions import grad_to_rad
from geometry_msgs.msg import Twist


def stop(vel: Twist, pub: rospy.Publisher):
    vel.linear.x = 0
    vel.anagular.z = 0
    pub.publish(vel)


def to_right(grad, vel: Twist, pub: rospy.Publisher, max_speed=0.5):
    vel.linear.x = 0
    vel.anagular.z = -max_speed
    pub.publish(vel)
    rospy.sleep(grad_to_rad(grad) / abs(max_speed))


def to_left(grad, vel: Twist, pub: rospy.Publisher, max_speed=0.5):
    vel.linear.x = 0
    vel.anagular.z = max_speed
    pub.publish(vel)
    rospy.sleep(grad_to_rad(grad) / abs(max_speed))


def forward(distance, vel: Twist, pub: rospy.Publisher, max_speed=0.1):
    vel.linear.x = max_speed
    vel.anagular.z = 0
    pub.publish(vel)
    rospy.sleep(distance / abs(max_speed))
