#!/usr/bin/env python
import rospy
import actionlib
from hw_t.msg import aruco_detectAction,aruco_detectGoal

def feedback_cb(msg):
        print("feedback:",msg)
def call_server():
   
    client2 = actionlib.SimpleActionClient('conveyor_pick', aruco_detectAction)
    client2.wait_for_server()
    goal = aruco_detectGoal()
    result = 0
    goal = aruco_detectGoal()
    goal.detect = 1
    client2.send_goal(goal, feedback_cb=feedback_cb)
    client2.wait_for_result()
    result = client2.get_result()
    print("the result is", result.distance_reached)
def call_dock():
    client3 = actionlib.SimpleActionClient('Table_dock', aruco_detectAction)
    client3.wait_for_server()
    goal = aruco_detectGoal()
    result = 0
    goal = aruco_detectGoal()
    goal.detect = 1
    rospy.set_param("/distance_goal_qr",goal.detect )

    client3.send_goal(goal, feedback_cb=feedback_cb)
    client3.wait_for_result()
    result = client3.get_result()
    print("the result is", result.distance_reached)

if __name__ == '__main__':

    try:
        rospy.init_node('action_client')
        # result = call_server()
        
        # print ('The result is:', result)
        result2=call_dock()
        print ('The result is:', result2)
    except rospy.ROSInterruptException as e:
        print ('Something went wrong:', e)