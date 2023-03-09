import rospy

from geometry_msgs.msg import Twist

rospy.init_node('move_node')

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

vel = Twist()
vel.linear.x = 0.05

pub.publish(vel)
rospy.sleep(1)

vel.linear.x = 0
vel.anagular.z = -0.5 # поворот

pub.publish(vel)
rospy.sleep(2)

vel.linear.x = 0.1
vel.anagular.z = 1
pub.publish(vel)
rospy.sleep(2)

vel.linear.x = 0
vel.anagular.z = 0
pub.publish(vel)
#
# rospy.Sunscriber("Welcome_topic")
#
# rospy.spin()
