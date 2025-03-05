#!/usr/bin/env python

from simulation.srv import Addtwoints,AddtwointsResponse
import rospy
from simulation.srv import *
import time
import rospy
from smach import State,StateMachine
from time import sleep
import actionlib
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from actionlib_msgs.msg import GoalID
import actionlib_msgs.msg
from geometry_msgs.msg import Twist
import redis
red=redis.Redis(host='localhost',port=6379)

from periphery import GPIO
import time
import smach_ros
green_pin = GPIO(23,"out")
grey_pin = GPIO(24,"out")
red2=redis.Redis(host='localhost',port=6379)
# green_pin = GPIO(23,"out")
# grey_pin = GPIO(24,"out")


def donecb(goalstatus,result):
	global done
	print("goal status: ",goalstatus)
	done= True

waypoints=[]
list1=[81,80]
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

class one(State):
    def __init__(self,position,orientation):
      
        State.__init__(self,outcomes=['cancelled','success','success1'], input_keys=['input'])
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
        # s.userdata.inpt=int(input("enter:"))
        return 'success'
    
class two(State):
        
        def __init__(self,position,orientation):
            global done
            done=False
            State.__init__(self,outcomes=['cancelled','success','success1'], input_keys=['input'])
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
            red.set('qr','go')
        
            while red.get('qr')!=b'success':
                pass
            rospy.loginfo("state one")
            return 'success1'

class three(State):
 
    def __init__(self):
        State.__init__(self,outcomes=['cancelled','success','success1'], input_keys=['input'])

    def execute(self, userdata):
        sleep(1)
        patrol.userdata.inpt=int(input("enter:"))
        if userdata.input == 1:
                return 'success1'
        elif userdata.input==2:
                return 'success'
class back(State):
    def __init__(self):
        State.__init__(self,outcomes=['success'])


    def execute(self, userdata):
        cmd_vel_pub = rospy.Publisher('/robot/cmd_vel',Twist, queue_size=1)
        twist = Twist()
        count=0
        while count!=10:
            time.sleep(1)
            twist.linear.x = -0.2
            cmd_vel_pub.publish(twist)
            count+=1
        return "success"

class camera_qr(State):
    def __init__(self):
        State.__init__(self,outcomes=['done'])

    def execute(self, userdata):
        rospy.wait_for_service('add_two_ints')
        try:
            s=rospy.ServiceProxy('add_two_ints',Addtwoints)
            res=s(1)
            print(res)
            
        except rospy.ServiceException as e:
            print("service call failed: %s"%e)
   

        return 'done'
            

class pick(State):
    def __init__(self):
        State.__init__(self,outcomes=['picking'])


    def execute(self, userdata):
            red2.set("conveyor","forward")
            green_pin.write(True)
            grey_pin.write(True) 
            # while True:
            #     if red.get("taurus_conv")=="stop":            
            #         green_pin.write(False)
            #         grey_pin.write(False)
            #         red.set("taurus_conv","go")
            #         break
            green_pin.write(False)
            grey_pin.write(False)
            return 'picking'


class drop(State):
    def __init__(self):
        State.__init__(self,outcomes=['dropping'])


    def execute(self, userdata):
          
          red2.set("conveyor","reverse")
          green_pin.write(True)
          while red.get('conveyor')!=b'hold':
            pass
               
          red2.set("conveyor","hold")
          green_pin.write(False)
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



if __name__ == '__main__':
    rospy.init_node('patrol')
    global patrol
    patrol = StateMachine(['success','success1','cancelled'])
    
    with patrol:
        print("state execution")
        StateMachine.add('ONE',one(waypoints[0][0],waypoints[0][1]),transitions={'success1':'DROP','success':'TWO','cancelled':'THREE'},remapping={'input':'inpt'})
        StateMachine.add('TWO',two(waypoints[1][0],waypoints[1][1]),transitions={'success1':'BACK','success':'PICK','cancelled':'THREE'},remapping={'input':'inpt'})
        StateMachine.add('THREE',three(),transitions={'success1':'ONE','success':'TWO','cancelled':'THREE'},remapping={'input':'inpt'})
        StateMachine.add('PICK',pick(),transitions={'picking':'TWO'})
        StateMachine.add('DROP',drop(),transitions={'dropping':'BACK'})
        StateMachine.add('BACK',back(),transitions={'success':'ONE'})
            
    sa=smach_ros.IntrospectionServer('s_server',patrol,'/SM_ROOT')
    sa.start()
    patrol.execute()
    rospy.spin()
    sa.stop()
        data=AddtwointsResponse()
    if  s==1:
        li1.move_up()
        data.ok=s
    elif s==2:
        li.forward()
        li.startJog()
        time.sleep(2)
        li.stopJog()
        print("forward")
        data.ok=s
    elif s==3:
        li1.move_down()
        data.ok=s
    elif s==4:
        li.reverse()
        li.startJog()
        time.sleep(2)
        li.stopJog()
        print("reverse")
        data.ok=s
    return data
  
def conveyor_server():
    rospy.init_node('conveyor')
    s = rospy.Service('conveyor_op', Addtwoints, conveyor_op)
    print("Ready to add two ints.")
    rospy.spin()

if __name__ == "__main__":
    conveyor_server()