#!/usr/bin/env python3
import rospy
from smach import State,StateMachine
from time import sleep
import actionlib
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from actionlib_msgs.msg import GoalID
import actionlib_msgs.msg
import move3 as conv2
import redis
red=redis.Redis(host='localhost',port=6379)
import redis
from periphery import GPIO
import time
green_pin = GPIO(22,"out")
grey_pin = GPIO(27,"out")
#red=redis.Redis(host='localhost',port=6379)
green_pin = GPIO(22,"out")
grey_pin = GPIO(27,"out")

'''waypoints = [
[(-0.115000143647, -2.01999998093, 0.0), (0.0, 0.0,  0.202661362435, 0.979248881631)],
[(1.83499968052, -0.0300001874566, 0.0), (0.0, 0.0,  0.999986985462,0.00510185332993)],
[(-1.839999794960022, -0.11999978870153427, 0.0), (0.0, 0.0, 0.6562120517716888,0.754576532307751)]

]'''
waypoints=[]
list1=[54,55]
def movebase_client(x):
            global waypoints,list1
            m1=[]
            file= open(r"/home/taurus1/testbot_ws/src/hw_t/goals/goal_"+str(x)+".txt", "r")
            l=[]
            t1=()
            t2=()
            l3=[]
            l4=[]
            l5=[]
            for i in range(0,10):
                l=l+[file.readline()]
            l=l[-1:-3:-1]
            s=float(l[0][7:-1])
            m=float(l[1][7:-1])
            l3.append(m)
            l3.append(s)
            l3.append(0.0)
            t1=(tuple(l3))
            l2=[]
            for i in range(0,6):
                l2=l2+[file.readline()]
            l2=l2[-1:-3:-1]
            z=float(l2[0][7:-1])
            w=float(l2[1][7:-1])
            l4.append(0.0)
            l4.append(0.0)
            l4.append(w)
            l4.append(z)
            t2=(tuple(l4))
            l5.append(t1)
            l5.append(t2)
            m1.append(l5)
            return m1[0]
for i in list1:
       
    waypoints.append(movebase_client(i))
print(waypoints)
	 

class waypoint(State):
    def __init__(self, position, orientation):
      
        State.__init__(self,outcomes=['success','aborted','done'])

        self.client=actionlib.SimpleActionClient('move_base',MoveBaseAction)
        self.client.wait_for_server()
        # print(position[0][0])

        self.goal=MoveBaseGoal()
        self.goal.target_pose.header.frame_id='map'
        self.goal.target_pose.pose.position.x = position[0]
        self.goal.target_pose.pose.position.y = position[1]
        self.goal.target_pose.pose.position.z = position[2]
        self.goal.target_pose.pose.orientation.x = orientation[0]
        self.goal.target_pose.pose.orientation.y = orientation[1]
        self.goal.target_pose.pose.orientation.z = orientation[2]
        self.goal.target_pose.pose.orientation.w = orientation[3]

    def execute(self, ud):
        if red.get("taurus")==b"pause":
            input("enter something go next goal")
            red.set("taurus","junk")
        self.client.send_goal(self.goal)
        self.client.wait_for_result()
        return 'success'


class up(State):
      
        def __init__(self):
            State.__init__(self,outcomes=['success','aborted','done'])
        def execute(self, ud):
           
           conv2.move_up()
           sleep(25)
    
           return 'success'
class waypoint1(State):
    def __init__(self, position, orientation):
      
        State.__init__(self,outcomes=['success','aborted','done'])

        self.client=actionlib.SimpleActionClient('move_base',MoveBaseAction)
        self.client.wait_for_server()
        # print(position[0][0])

        self.goal=MoveBaseGoal()
        self.goal.target_pose.header.frame_id='map'
        self.goal.target_pose.pose.position.x = position[0]
        self.goal.target_pose.pose.position.y = position[1]
        self.goal.target_pose.pose.position.z = position[2]
        self.goal.target_pose.pose.orientation.x = orientation[0]
        self.goal.target_pose.pose.orientation.y = orientation[1]
        self.goal.target_pose.pose.orientation.z = orientation[2]
        self.goal.target_pose.pose.orientation.w = orientation[3]

    def execute(self, ud):
        # while True:
        #     if red.get("taurus")==b"move":
        #         self.client.send_goal(self.goal)
        #         self.client.wait_for_result()
        #         red.set("taurus","junk")
        #         break
        if red.get("taurus")==b"pause":
            input("enter something go next goal")
            red.set("taurus","junk")
        self.client.send_goal(self.goal)
        self.client.wait_for_result()
        return 'success'



class cancel(State):
        def __init__(self):
            State.__init__(self,outcomes=['success','aborted','done'])
        def execute(self, ud):
           
           pub_cancel_goal = rospy.Publisher('move_base/cancel', GoalID, queue_size=1)
           rospy.init_node('simp', anonymous=True)
           count = 0

           rate = rospy.Rate(10) # 10hz
           while not rospy.is_shutdown():
            pub_cancel_goal.publish()
        # sleep(5)
        # print("executed cancel goal")
            count+=1
            if count >= 5:
                print("sdf")
                break
        
            rate.sleep()
        
            return 'success'



class down(State):
      
        def __init__(self):
            State.__init__(self,outcomes=['success','aborted','done'])


        def execute(self, ud):
          
           conv2.move_down()
           sleep(25)
        
           return 'success'  

class forward(State):
      
        def __init__(self):
            State.__init__(self,outcomes=['forward'])
        def execute(self, userdata):
    
                green_pin.write(True)
                sleep(2)
                green_pin.write(False)

                return 'forward'

class reverse(State):
      
        def __init__(self):
            State.__init__(self,outcomes=['reverse','aborted','done'])


        def execute(self, userdata):
            green_pin.write(True)
            grey_pin.write(True)
            sleep(2)
            green_pin.write(False)
            grey_pin.write(False)
               
            return 'reverse' 
        



if __name__ == '__main__':
    rospy.init_node('patrol')
    patrol = StateMachine(['success','aborted','done'])
    
    with patrol:
        print("state execution")
        StateMachine.add('TWO', waypoint(waypoints[1][0],waypoints[1][1]), transitions={'success':'UP'})
        StateMachine.add('FORWARD', forward(), transitions={'forward':'TWO'})
        StateMachine.add('REVERSE', reverse(), transitions={'reverse':'ONE'})
        StateMachine.add('UP', up(), transitions={'success':'REVERSE'})
        #StateMachine.add('TWO', waypoint(waypoints[1][0],waypoints[1][1]), transitions={'success':'UP'})
        StateMachine.add('ONE', waypoint1(waypoints[0][0],waypoints[0][1]), transitions={'success':'DOWN'})
        StateMachine.add('DOWN', down(), transitions={'success':'FORWARD'})
     
        
            
    patrol.execute()
        