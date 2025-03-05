#!/usr/bin/env python3
import rospy
import actionlib
from smach import State,StateMachine
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
waypoints = [
['one', (3.6192455291748047, 7.483279228210449), (0.0, 0.0, -0.7550899263595832, 0.6556212344870164)],
['two', (3.025996208190918, -0.5646624565124512), (0.0, 0.0, -0.7089192248631052, 0.7052896799326459)],
['three', (0.2601318359375, 7.332136631011963), (0.0, 0.0,  -0.00965651948991638,  0.9999533747287125)]
]
class Waypoint(State):
    def __init__(self, position, orientation):
        State.__init__(self, outcomes=['success'])
# Get an action client
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()
# Define the goal
        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.pose.position.x = position[0]
        self.goal.target_pose.pose.position.y = position[1]
        self.goal.target_pose.pose.position.z = 0.0
        self.goal.target_pose.pose.orientation.x = orientation[0]
        self.goal.target_pose.pose.orientation.y = orientation[1]
        self.goal.target_pose.pose.orientation.z = orientation[2]
        self.goal.target_pose.pose.orientation.w = orientation[3]
    def execute(self, userdata):
        self.client.send_goal(self.goal)
        self.client.wait_for_result()
        return 'success'
class canclegoal(State):
    def __init__(self):

        State.__init__(self,outcomes=)
if __name__ == '__main__':
    rospy.init_node('patrol')
    patrol = StateMachine('success')
    with patrol:
        for i,w in enumerate(waypoints):
            StateMachine.add(w[0],Waypoint(w[1], w[2]),transitions={'success':waypoints[(i + 1) % len(waypoints)][0]})
    patrol.execute()
