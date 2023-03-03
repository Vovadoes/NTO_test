import rospy

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

rospy.init_node('one_meter_node')

pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
def callback_regulator(msg):
    vel = Twist()

    if msg.pose.pose.position.x >= 1:
        vel.linear.x = 0
    else:
        vel.linear.x = 0.1
    pub.publish(vel)

rospy.Sunscriber("/odom", Odometry, callback_regulator)

rospy.spin()
