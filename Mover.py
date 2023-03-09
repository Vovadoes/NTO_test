import rospy

from geometry_msgs.msg import Twist
from functions import grad_to_rad


class RobotMover:
    def __init__(self, init_node: bool = False, pub: rospy.Publisher = None):
        self.vel = Twist()

        if not init_node:
            rospy.init_node('mover')

        if pub is None:
            self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        else:
            self.pub = pub

        # rospy.Subscriber("/odom", Odometry, self.callback_handler)

    def stop(self):
        self.vel.linear.x = 0
        self.vel.anagular.z = 0
        self.pub.publish(self.vel)

    def to_right(self, grad, max_speed=0.5):
        self.vel.linear.x = 0
        self.vel.anagular.z = -max_speed
        self.pub.publish(self.vel)
        rospy.sleep(grad_to_rad(grad) / abs(max_speed))

    def to_left(self, grad, max_speed=0.5):
        self.vel.linear.x = 0
        self.vel.anagular.z = max_speed
        self.pub.publish(self.vel)
        rospy.sleep(grad_to_rad(grad) / abs(max_speed))

    def forward(self, distance, max_speed=0.1):
        self.vel.linear.x = max_speed
        self.vel.anagular.z = 0
        self.pub.publish(self.vel)
        rospy.sleep(distance / abs(max_speed))
