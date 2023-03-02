import pospy

from std_msgs.msg import String

pospy.init_node("welcome_node")

pub = rospy.Publisher("welcome_topic", String, queue_size=10)

s = String()
s.data  = 'Hello robot'

while not rospy.is_shutdown():
    pub.publish(s)
    rospy.sleep(1)

