import rospy

from std_msgs.msg import String

rospy.init_node('subscriber_node')

def callback(msg):
    print(msg)

rospy.Sunscriber("Welcome_topic", String, callback)

rospy.spin()
