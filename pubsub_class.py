import rospy

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class RobotMover:
    def __init__(self):
        self.distance_passed = None
        self.vel = Twist()
        rospy.itit_node('one_meter_node')

        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

        rospy.Sunscriber("/odom", Odometry, self.callback_handler)

    def callback_handler(self, msg):
        self.distance_passed = msg.pose.pose.position.x

    def vel_publisher(self, value):
        self.vel.linear.x = value
        self.pub.publish(self.vel)

    def regulator(self):
        print(self.distance_passed)
        if self.distance_passed >= 1:
            self.vel_publisher(0)

r = RobotMover()
while not rospy.is_shutdown():
    rospy.sleep(0.5)
    r.regulator()


rospy.spin()
