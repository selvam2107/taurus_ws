#!/usr/bin/env python3.6
import rospy
from smach import State,StateMachine
from time import sleep
import actionlib
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from actionlib_msgs.msg import GoalID
import actionlib_msgs.msg
import conv
from geometry_msgs.msg import Twist
import redis
red=redis.Redis(host='192.168.5.11',port=6379)
red3=redis.Redis(host='localhost',port=6379)
# from periphery import GPIO
# import time
# import smach_ros
# green_pin = GPIO(23,"out")
# grey_pin = GPIO(24,"out")
red2=redis.Redis(host='192.168.5.51',port=6379)
# green_pin = GPIO(23,"out")
# grey_pin = GPIO(24,"out")


def donecb(goalstatus,result):
	global done
	
	print("goal status: ",goalstatus)

	done= True

waypoints=[]
list1=[12,13]
def movebase_client(x):
            global waypoints,list1
            m1=[]
            file= open(r"/home/bot/testbot_ws/src/hw_t/goals/goal_"+str(x)+".txt", "r")
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
        # time.sleep(5)
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
    
# class two(State):
        
#         def __init__(self,position,orientation):
#             global done
#             done=False
#             State.__init__(self,outcomes=['cancelled','success','success1'], input_keys=['input'])
#             self.client=actionlib.SimpleActionClient('move_base',MoveBaseAction)
#             self.client.wait_for_server()
#             #red.set("taurus","junk")

#             self.goal=MoveBaseGoal()
#             self.goal.target_pose.header.frame_id='map'
#             self.goal.target_pose.pose.position.x = position[0]
#             self.goal.target_pose.pose.position.y = position[1]
#             self.goal.target_pose.pose.position.z = position[2]
#             self.goal.target_pose.pose.orientation.x = orientation[0]
#             self.goal.target_pose.pose.orientation.y = orientation[1]
#             self.goal.target_pose.pose.orientation.z = orientation[2]
#             self.goal.target_pose.pose.orientation.w = orientation[3]



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
        patrol.userdata.inpt=int(input("enter:"))
        if userdata.input == 1:
                return 'success1'
        elif userdata.input==2:
                return 'success'
class rotate(State):
    def __init__(self):
        State.__init__(self,outcomes=['success'])


    def execute(self, userdata):
        # cmd_vel_pub = rospy.Publisher('/robot/cmd_vel',Twist, queue_size=1)
        # twist = Twist()
        count=0
        red.set('srotate','go')
        while red.get('srotate')==b'go':
            pass
        return "success"
class back(State):
    def __init__(self):
        State.__init__(self,outcomes=['success'])


    def execute(self, userdata):
        cmd_vel_pub = rospy.Publisher('/robot/cmd_vel',Twist, queue_size=1)
        twist = Twist()
        count=red3.get('distance')
        count=int(count)
        print(coun,type(count))
        while count<=1800:
            # time.sleep(1)
            twist.linear.x = -0.2
            cmd_vel_pub.publish(twist)
            count=red.get('distance')
            count=int(count)
            
            # count+=1
        
        return "success"
class rotate1(State):
    def __init__(self):
        State.__init__(self,outcomes=['success'])


    def execute(self, userdata):
        # cmd_vel_pub = rospy.Publisher('/robot/cmd_vel',Twist, queue_size=1)
        twist = Twist()
        count=0
        while red.get('srotate3')!=b'go':
            pass
        # red.set('srotate1','go')
        while red.get('srotate3')==b'go':
            pass
        return "success" 
class rotate3(State):
    def __init__(self):
        State.__init__(self,outcomes=['success'])


    def execute(self, userdata):
        # cmd_vel_pub = rospy.Publisher('/robot/cmd_vel',Twist, queue_size=1)
        twist = Twist()
        count=0
        red.set('srotate1','go')
        while red.get('srotate1')==b'go':
            pass
        return "success"  
class tele(State):
    def __init__(self):
        State.__init__(self,outcomes=['success'])


    def execute(self, userdata):
        client3 = actionlib.SimpleActionClient('Table_dock', aruco_detectAction)
        client3.wait_for_server()
        goal = aruco_detectGoal()
        result = 0
        goal = aruco_detectGoal()
        goal.detect = 1
        client3.send_goal(goal, feedback_cb=feedback_cb)
        client3.wait_for_result()
        result = client3.get_result()
        print("the result is", result.distance_reached)
        return 'success'
 

class pick(State):
    def __init__(self):
        State.__init__(self,outcomes=['picking'])


    def execute(self, userdata):
            # red2.set("conveyor","forward")
            while red.get('ssapl')!=b'go':
                pass
            conv.write1()
            red.set('taurus','go')
            conv.startJog()
            while red.get("ssapl")!=b'stop':
                pass
            conv.stopJog()

            return 'picking'
class camera_qr(State):
    def __init__(self):
        State.__init__(self,outcomes=['cancelled','success','success1'], input_keys=['input'])
    def execute(self, userdata):
        red3.set('qr','go')
        while red3.get('qr')==b'go':
            pass
        return 'success'

# class drop(State):
#     def __init__(self):
#         State.__init__(self,outcomes=['dropping'])


#     def execute(self, userdata):
          
#           red2.set("conveyor","reverse")
#           green_pin.write(True)
#           sleep(2)
               
#           red2.set("conveyor","hold")
#           green_pin.write(False)
#           return 'dropping'
class drop(State):
    def __init__(self):
        State.__init__(self,outcomes=['dropping'])


    def execute(self, userdata):
            # red2.set("conveyor","forward")
            while red.get('ssapl')!=b'go':
                pass
            conv.write()
            # red.set('taurus','go')
            conv.startJog()
            while red.get("ssapl")!=b'stop':
                pass
            conv.stopJog()

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
        
        StateMachine.add('ONE',one(waypoints[0][0],waypoints[0][1]),transitions={'success1':'TELE','success':'ROTATE'},remapping={'input':'inpt'})
        StateMachine.add('TWO',two(waypoints[1][0],waypoints[1][1]),transitions={'success1':'ROTATE1','success':'ONE','cancelled':'THREE'},remapping={'input':'inpt'})
        StateMachine.add('TELE',tele(),transitions={'success':'TWO'})
        # StateMachine.add('THREE',three(),transitions={'success1':'ONE','success':'TWO','cancelled':'THREE'},remapping={'input':'inpt'})
        StateMachine.add('PICK',pick(),transitions={'picking':'ROTATE3'})
        StateMachine.add('DROP',drop(),transitions={'dropping':'back'})
        StateMachine.add('ROTATE3',rotate1(),transitions={'success':'ONE'})
        StateMachine.add('back',back(),transitions={'success':'ROTATE3'})
        # StateMachine.add('ROTATE2',rotate(),transitions={'success':'TWO'})
        StateMachine.add('ROTATE',rotate3(),transitions={'success':'CAMERA'})
        StateMachine.add('CAMERA',camera_qr(),transitions={'success':'ROTATE4'})
        StateMachine.add('ROTATE4',rotate3(),transitions={'success':'DROP'})
        # StateMachine.add('TELE',tele(),transitions={'success':'PICK'})
            
    # sa=smach_ros.IntrospectionServer('s_server',patrol,'/SM_ROOT')
    # sa.start()
    patrol.execute()
    rospy.spin()
    # sa.stop()
        