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
# from pymodbus.client import ModbusSerialClient as client

# import move2 as conv2
import redis
red=redis.Redis(host='localhost',port=6379)




waypoints = []

list1=[54,55]
def movebase_client(x):
            global waypoints,list1
            m1=[]
            file= open(r"/home/av/testbot_ws/src/hw_t/goals/goal_"+str(x)+".txt", "r")
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


def donecb(goalstatus,result):
	global done
	
	print("goal status: ",goalstatus)

	done= True

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
            # print('goal not done')
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
            rospy.loginfo("state one")
            return 'success1'

class three(State):
 
    def __init__(self):
        State.__init__(self,outcomes=['cancelled','success','success1'], input_keys=['input'])

    def execute(self, userdata):
        sleep(1)
        s.userdata.inpt=int(input("enter:"))
        if userdata.input == 1:
                return 'success1'
        elif userdata.input==2:
                return 'success'
    
    
        
class pick(State):
    def __init__(self):
        State.__init__(self,outcomes=['picking'])


    def execute(self, userdata):
   
            move.write1()
            move.startJog()
            sleep(4)
            move.stopJog()
            # print("hiii")
            return 'picking'
          
class drop(State):
    def __init__(self):
        State.__init__(self,outcomes=['dropping'])


    def execute(self, userdata):
     
          move3.write()
          move3.startJog()
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
  


def main():

    rospy.init_node("patrol")
    global s
    s=StateMachine(outcomes=['success','success1','cancelled'])
    
    # s.use
    # rdata.inpt=int(input("enter:"))
    with s:
        StateMachine.add('ONE',one(waypoints[0][0],waypoints[0][1]),transitions={'success1':'DROP','success':'PICK','cancelled':'THREE'},remapping={'input':'inpt'})
        StateMachine.add('TWO',two(waypoints[1][0],waypoints[1][1]),transitions={'success1':'DROP','success':'PICK','cancelled':'THREE'},remapping={'input':'inpt'})
        StateMachine.add('THREE',three(),transitions={'success1':'PICK','success':'DROP','cancelled':'THREE'},remapping={'input':'inpt'})
        StateMachine.add('PICK',pick(),transitions={'picking':'TWO'})
        StateMachine.add('DROP',drop(),transitions={'dropping':'ONE'})


    sa=smach_ros.IntrospectionServer('s_server',s,'/SM_ROOT')
    sa.start()
    s.execute()
    rospy.spin()
    sa.stop()
if __name__=="__main__":
    main()
    