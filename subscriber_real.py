import rospy

from sensor_msgs.msg import LaserScan

rospy.itit_node('scan_node')

def scan_cb(scan):
    print(scan.ranges[0])

rospy.Sunscriber("scan", LaserScan, scan_cb)

rospy.spin()
