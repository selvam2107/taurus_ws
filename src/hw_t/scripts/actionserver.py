#! /usr/bin/env python3

import rospy
import actionlib
from hw_t.msg import distanceAction, distanceFeedback, distanceResult


class ActionServer():

    def __init__(self):
        self.a_server = actionlib.SimpleActionServer(
            "find_distance", distanceAction, execute_cb=self.execute_cb, auto_start=False)
        self.a_server.start()
        print("-----------------")

    def execute_cb(self, goal):

        # success = True
        reached= ''
        feedback = distanceFeedback()
        result = distanceResult()
        rate = rospy.Rate(1)
        print("-----------------",goal.qr)

        for i in range(0, goal.qr):
            # if goal.qr!=10:
            # if self.a_server.is_preempt_requested():
            #     self.a_server.set_preempted()
            #     success = False
            #     break
        
            # if goal.qr==1:
                reached =str(i)
                feedback.reached= reached

            
                self.a_server.publish_feedback(feedback)
                rate.sleep()

        result.distance_reached="dgh"
        self.a_server.set_succeeded(result)


if __name__ == "__main__":
    rospy.init_node("action_server")
    s = ActionServer()
    rospy.spin()