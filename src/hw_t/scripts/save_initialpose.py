#! /usr/bin/env python
import rospy
import time
from geometry_msgs.msg import PoseWithCovarianceStamped
def call_back(msg):
    print(msg)
    file= open(r"/root/testbot_ws/src/hw_t/goals/initialpose)"+".txt", "w")
    file.write(str(msg))
    file.close()

if __name__ == '__main__':
    time.sleep(10)
    rospy.init_node("pose_saver")
    s=rospy.Subscriber("amcl_pose",PoseWithCovarianceStamped,call_back,queue_size=10)
    rospy.spin()
