import rospy

from rospy_tutorials import AddTwoInts, AddTwoIntsPresponse

rospy.init_node('add_two_ints_server')

def handle_callculation(req):
    print(f"Returning [{req.a, req.b, (req.a + req.b)}]")
    return AddTwoIntsResponse(req.a + req.b)

rospy.Service('sum_service', AddTwoInts, handle_callculation)

rospy.spin()
