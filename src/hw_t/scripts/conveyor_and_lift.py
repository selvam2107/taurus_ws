#!/usr/bin/env python3
import rospy
from smach import State,StateMachine
from time import sleep
import actionlib
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from actionlib_msgs.msg import GoalID
import smach_ros 
import move3 as move2
import redis
import smach_ros
from geometry_msgs.msg import Twist

import redis
# from periphery import GPIO
# import time
# green_pin = GPIO(23,"out")
# grey_pin = GPIO(24,"out")
global red
# red=redis.Redis(host='192.168.5.86',port=6379)
red2=redis.Redis(host='192.168.5.86',port=6379)



class pick1(State):
    def __init__(self):
        State.__init__(self,outcomes=['picking1'])


    def execute(self, userdata):
            red.set("conveyor","forward")
       
            move2.write()
            move2.startJog()
            input("enter something:")
            red.set("conveyor","hold")
            move2.stopJog()
            return 'picking1'
    
class drop1(State):
    def __init__(self):
        State.__init__(self,outcomes=['dropping1'])


    def execute(self, userdata):
          input("enter something:")
          red.set("conveyor","reverse")
          move2.write1()
          move2.startJog()
          
          input("enter something:")
          red2.set("conveyor","hold")
          move2.stopJog()
          return 'dropping1'
    

class pick2(State):
    def __init__(self):
        State.__init__(self,outcomes=['picking2'])


    def execute(self, userdata):
            red2.set("conveyor","forward")
            move2.write1()
            move2.startJog()
           
            red2.set("conveyor","hold")
            move2.stopJog()
            return 'picking2'
    

class drop2(State):
    def __init__(self):
        State.__init__(self,outcomes=['dropping2'])


    def execute(self, userdata):
          
          red2.set("conveyor","reverse")
          move2.write()
          move2.startJog()
          
          input("enter something:")
          red2.set("conveyor","hold")
          move2.stopJog()
          return 'dropping2'
    




# class up(State):
#         def __init__(self):
#             State.__init__(self,outcomes=['up'])
#         def execute(self, userdata):
    
#                 green_pin.write(True)
#                 sleep(5)
#                 green_pin.write(False)

#                 return 'up'

# class down(State):
      
#         def __init__(self):
#             State.__init__(self,outcomes=['success','aborted','done'])


#         def execute(self, userdata):
#             green_pin.write(True)
#             grey_pin.write(True)
#             sleep(5)
# #             green_pin.write(False)
# #             grey_pin.write(False)
               
#             return 'down' 
        


  


def main():

    rospy.init_node("patrol")
    global s
    s=StateMachine(outcomes=['success','success1','cancelled'])
    
   
    with s:
        # StateMachine.add('UP',pick(),transitions={'picking':'PICK'})
        # StateMachine.add('PICK1',pick1(),transitions={'picking1':'DROP2'})
        # StateMachine.add('DROP1',drop1(),transitions={'dropping1':'PICK1'})
        StateMachine.add('PICK2',pick2(),transitions={'picking2':'DROP2'})
        StateMachine.add('DROP2',drop2(),transitions={'dropping2':'PICK2'})
        # StateMachine.add('DOWN', down(), transitions={'down':'drop'})
    sa=smach_ros.IntrospectionServer('s_server',s,'/SM_ROOT')
    sa.start()
    s.execute()
    rospy.spin()
    sa.stop()
if __name__=="__main__":
    main()
    