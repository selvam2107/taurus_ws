#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
import math
import actionlib
import redis
import time
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped
from time import sleep
import actionlib
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from actionlib_msgs.msg import GoalID,GoalStatusArray
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
rospy.init_node("waypoint")

class follower:
    def __init__(self):
        print("fhi3")
        self.goal = PoseStamped()
        self.goals = []
        self.odom = Odometry()
        self.dist = 0
        self.latch = 0
        self.msg1=''
        self.sub_goal = rospy.Subscriber("/move_base_simple/goal", PoseStamped, self.callback_goal)
        self.sub = rospy.Subscriber('/mcl_pose',PoseStamped, self.callback_odom)
        self.pub_goal = rospy.Publisher("/desired_local_planner", String, queue_size = 1)
    def callback_goal(self, message):
        self.goal = message
        self.goals=[]
        self.goals.append(self.goal)
        # print(message)/desired_local_planner
    def callback_odom(self, message):
       # print(message)
       # print(self.goals)
        self.odom = message
        count=0
        if (len(self.goals) != 0 ):
            self.dist = math.sqrt((self.goals[0].pose.position.x - self.odom.pose.position.x)**2 + (self.goals[0].pose.position.y - self.odom.pose.position.y)**2)
            if (self.dist > 1 ) and self.latch==0:
                
                    self.msg1="teb"
                    self.pub_goal.publish(self.msg1)
                    self.latch = 2
                    
                    print(self.dist)
                    
            else:
                if self.dist <= 1 and self.latch == 2:
                    self.msg1="dwa"
                    self.pub_goal.publish(self.msg1)
                    self.latch = 0
                    count=0
            print(self.dist,"wfe2")
follower = follower()
rospy.spin()
print("\nNode shutdown\n")