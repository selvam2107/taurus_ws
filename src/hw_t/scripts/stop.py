#!/usr/bin/env python3
import rospy
from smach import State,StateMachine
from time import sleep
import actionlib
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from actionlib_msgs.msg import GoalID
import smach_ros 

# from pymodbus.client import ModbusSerialClient as client

# import move2 as conv2
import redis
red=redis.Redis(host='localhost',port=6379)
red1=redis.Redis(host='192.168.7.156',port=6379)



import smach_ros 
waypoints = [
[(-5.605243682861328, -2.2213077545166016, 0.0), (0.0, 0.0,  -0.07574386923184367,  0.997127306954227)],
[(0.85162353515625,  -2.9363155364990234, 0.0), (0.0, 0.0,   0.9990924376920979,0.042594611706899176)]
]



def donecb(goalstatus,result):
	global done
	
	print("goal status: ",goalstatus)
	done= True

class one(State):
    def __init__(self,position,orientation):
      
        State.__init__(self,outcomes=['cancelled','success','success1'], input_keys=['input'])
        self.client=actionlib.SimpleActionClient('move_base',MoveBaseAction)
        self.client.wait_for_server()
        

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
            #print('goal not done')
            if red.get("taurus")==b'pause':
                print('cancel goal')
                talker()
                red.set("taurus","junk")
                return 'cancelled'
        self.client.wait_for_result()
        rospy.loginfo("state one")
        if self.client.get_goal_status_text !="Goal reached.":
             red1.set("conveyor","reverse")
        # else:
        #      red1.set("conveyor","hold")
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
        s.userdata.input=int(input("enter:"))
        if userdata.input == 1:
                rospy.loginfo("----------------------> state one")
                return 'success1'
        elif userdata.input==2:
                rospy.loginfo("----------------------> state two")
                return 'success'
    
    
        


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
    
# def battery():
    
#         v=(read1.getRegister(49))/100
#         if v<20:
#             print("Battery about to die please put a charge")
#             return 'recharge'
       
            


def main():

    rospy.init_node("patrol")
    # mod = client(method='rtu', timeout=2, parity='N', baudrate=115200,port='/dev/ttyUnotSB0')
    # print(mod.connect())
    # global read1
    # read1= mod.read_holding_registers(address= 0, count=58, unit= 1)
    global s
    
    s=StateMachine(outcomes=['success','success1','cancelled'])
    s.userdata.inpt =0
    
    # s.use
    # rdata.inpt=int(input("enter:"))
    with s:
        StateMachine.add('ONE',one(waypoints[0][0],waypoints[0][1]),transitions={'success1':'ONE','success':'TWO','cancelled':'THREE'},remapping={'inpt':'input'})
        StateMachine.add('TWO',two(waypoints[1][0],waypoints[1][1]),transitions={'success1':'ONE','success':'TWO','cancelled':'THREE'},remapping={'inpt':'input'})
        StateMachine.add('THREE',three(),transitions={'success1':'ONE','success':'TWO','cancelled':'THREE'},remapping={'inpt':'input'})
    sa=smach_ros.IntrospectionServer('s_server',s,'/SM_ROOT')
    sa.start()
    s.execute()
    rospy.spin()
    sa.stop()
if __name__=="__main__":
    main()
    