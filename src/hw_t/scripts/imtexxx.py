#!/usr/bin/env python3
import rospy
from smach import State,StateMachine
from time import sleep
import actionlib
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from actionlib_msgs.msg import GoalID
import smach_ros 
import move2,move
import redis
import smach_ros
from geometry_msgs.msg import Twist

import redis
from periphery import GPIO
import time
green_pin = GPIO(23,"out")
grey_pin = GPIO(24,"out")
red=redis.Redis(host='localhost',port=6379)
green_pin = GPIO(23,"out")
grey_pin = GPIO(24,"out")



waypoints = [
[(-0.115000143647, -2.01999998093, 0.0), (0.0, 0.0,  0.202661362435, 0.979248881631)],
[(1.83499968052, -0.0300001874566, 0.0), (0.0, 0.0,  0.999986985462,0.00510185332993)]
]



def donecb(goalstatus,result):
	global done
	
	print("goal status: ",goalstatus)

	done= True

class one(State):
    def __init__(self,position,orientation):
      
        State.__init__(self,outcomes=['cancelled','success','success1','goal1','goal2'], input_keys=['input'])
        self.client=actionlib.SimpleActionClient('move_base',MoveBaseAction)
        self.client.wait_for_server()
        #red.set("taurus","junk")

        self.goal=MoveBaseGoal()
        self.goal.target_pose.header.frame_id='map'
        self.goal.target_pose.pose.position.x = position[0]
        self.goal.target_pose.pose.position.y = position[1]
        self.goal.target_pose.pose.position.z = position[2]
        self.goal.target_pose.pose.orientation.x = orientation[0]
        self.goal.target_pose.pose.orientation.y = orientation[1]
        self.goal.target_pose.pose.orientation.z = orientation[2]
        self.goal.target_pose.pose.orientation.w = orientation[3]



    def execute(self, userdata):
        sleep(1)
        global done
        done=False
        self.client.send_goal(self.goal,done_cb=donecb)
        print("--------")
        while not done:
            print('goal not done')
            if red.get("taurus")==b'pause':
                print('cancel goal')
                talker()
                red.set("taurus","junk")
                return 'cancelled'
        self.client.wait_for_result()
        rospy.loginfo("state one")
        return 'success'
    
class two(State):
        
        def __init__(self,position,orientation):
            global done
            done=False
            State.__init__(self,outcomes=['cancelled','success','success1','goal1','goal2'], input_keys=['input'])
            self.client=actionlib.SimpleActionClient('move_base',MoveBaseAction)
            self.client.wait_for_server()
            #red.set("taurus","junk")

            self.goal=MoveBaseGoal()
            self.goal.target_pose.header.frame_id='map'
            self.goal.target_pose.pose.position.x = position[0]
            self.goal.target_pose.pose.position.y = position[1]
            self.goal.target_pose.pose.position.z = position[2]
            self.goal.target_pose.pose.orientation.x = orientation[0]
            self.goal.target_pose.pose.orientation.y = orientation[1]
            self.goal.target_pose.pose.orientation.z = orientation[2]
            self.goal.target_pose.pose.orientation.w = orientation[3]



        def execute(self, userdata):
            sleep(1)
            global done
            done=False
          
            self.client.send_goal(self.goal,done_cb=donecb)
            print("--------")
            while not done:
                # print('goal not done')
                if red.get("taurus")==b'pause':
                    print('cancel goal')
                    talker()
                    red.set("taurus","junk")
                    return 'cancelled'
            self.client.wait_for_result()
            rospy.loginfo("state one")
            return 'success1'

class three(State):
    def __init__(self):
        State.__init__(self,outcomes=['cancelled','success','success1','goal2','goal1'], input_keys=['input'])

    def execute(self, userdata):
        sleep(1)
        s.userdata.inpt=int(input("enter:"))
        if userdata.input == 1:
                return 'goal1'
        elif userdata.input == 2:
                return 'goal2'
    
    
        
class pick(State):
    def __init__(self):
        State.__init__(self,outcomes=['picking'])


    def execute(self, userdata):
   
            move.write1()
            move.startJog()
            sleep(4)
            move.stopJog()
            print("hiii")
            return 'picking'
          
class drop(State):
    def __init__(self):
        State.__init__(self,outcomes=['dropping'])


    def execute(self, userdata):
     
          move.write()
          move.startJog()
          sleep(4)
          move.stopJog()
          return 'dropping'


def talker():
    pub_cancel_goal = rospy.Publisher('move_base/cancel', GoalID, queue_size=1)
   
    count = 0

    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        pub_cancel_goal.publish()
        count+=1
        if count >= 5:
           
            break
       
        rate.sleep()

class up(State):
      
        def __init__(self):
            State.__init__(self,outcomes=['up'])
        def execute(self, userdata):
    
                green_pin.write(True)
                sleep(5)
                green_pin.write(False)

                return 'up'

class down(State):
      
        def __init__(self):
            State.__init__(self,outcomes=['success','aborted','done'])


        def execute(self, userdata):
            green_pin.write(True)
            grey_pin.write(True)
            sleep(5)
            green_pin.write(False)
            grey_pin.write(False)
               
            return 'down' 
        


  


def main():

    rospy.init_node("patrol")
    global s
    s=StateMachine(outcomes=['success','success1','cancelled'])
    
    # s.use
    # rdata.inpt=int(input("enter:"))
    with s:
        StateMachine.add('ONE',one(waypoints[0][0],waypoints[0][1]),transitions={'success1':'down','success':'up','cancelled':'THREE'},remapping={'input':'inpt'})
        StateMachine.add('TWO',two(waypoints[1][0],waypoints[1][1]),transitions={'success1':'down','success':'up','cancelled':'THREE'},remapping={'input':'inpt'})
        StateMachine.add('THREE',three(),transitions={'success1':'down','success':'up','cancelled':'THREE'},remapping={'input':'inpt'})
        StateMachine.add('PICK',pick(),transitions={'picking':'TWO'})
        StateMachine.add('DROP',drop(),transitions={'dropping':'ONE'})
        StateMachine.add('UP', up(), transitions={'up':'Pick'})
        StateMachine.add('down', down(), transitions={'down':'drop'})




    sa=smach_ros.IntrospectionServer('s_server',s,'/SM_ROOT')
    sa.start()
    s.execute()
    rospy.spin()
    sa.stop()
if __name__=="__main__":
    main()
    