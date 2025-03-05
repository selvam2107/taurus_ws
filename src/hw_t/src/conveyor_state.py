#!/usr/bin/env python3
import rospy
from smach import State,StateMachine
from time import sleep
import actionlib
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from actionlib_msgs.msg import GoalID
import smach_ros 
import redis
red=redis.Redis(host='localhost',port=6379)
import smach_ros 

from periphery import GPIO
import time
green_pin = GPIO(23,"out")
grey_pin = GPIO(24,"out")

class forward(State):
    def __init__(self):
      
        State.__init__(self,outcomes=['forward'])


    def execute(self, userdata):
        green_pin.write(True)
        sleep(5)
        green_pin.write(False)
        return 'forward'

class reverse(State):
    def __init__(self):
      
        State.__init__(self,outcomes=['reverse'])


    def execute(self, userdata):
        sleep(1)
        green_pin.write(True)
        grey_pin.write(True)
        sleep(5)
        green_pin.write(False)
        grey_pin.write(False)
        return 'reverse'
    



def main():

    rospy.init_node("patrol")

    
    s=StateMachine(outcomes=['success','success1','cancelled'])

    with s:
        StateMachine.add('FORWARD',forward(),transitions={'forward':'REVERSE'})
        StateMachine.add('REVERSE',reverse(),transitions={'reverse':'FORWARD'})
        
    s.execute()

if __name__=="__main__":
    main()
    
