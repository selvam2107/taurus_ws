#!/usr/bin/env python
import rospy
from smach import State,StateMachine
from time import sleep
import actionlib
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from actionlib_msgs.msg import GoalID
from simulation.srv import *
import redis
import smach_ros

red=redis.Redis(host='locahost',port=6379)


waypoints = [
[(-0.115000143647, -2.01999998093, 0.0), (0.0, 0.0,  0.202661362435, 0.979248881631)],
[(1.83499968052, -0.0300001874566, 0.0), (0.0, 0.0,  0.999986985462,0.00510185332993)]
]

def donecb(goalstatus,result):
    global donecb
    print("goal_status",goalstatus)
    done = True

class waypoint(State):
    def __init__(self, position, orientation):
      
        State.__init__(self,outcomes=['goal1','goal2','cancelled'], input_keys=['input'])

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

    def execute(self, ud):
        sleep(1)
        global done
        done = False
        self.client.send_goal(self.goal)
        while not done:
            print("goal not done")
            if red.get("taurus")==b'pause':
                print("cancelling the goal")
                paused()
                red.set("taurus","junk")
                return 'cancelled'
        self.client.wait_for_result()
        return 'goal1'

class waypoint1(State):
    def __init__(self, position, orientation):
      
        State.__init__(self,outcomes=['goal2','goal1','cancelled'], input_keys=['input'])

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

    def execute(self, ud):
        sleep(1)
        global done
        done=False
        self.client.send_goal(self.goal)
        while not done:
            print('goal not done')
            if red.get("taurus")==b'pause':
                    print('cancel goal')
                    paused()
                    red.set("taurus","junk")
                    return 'cancelled'
        self.client.wait_for_result()
        return 'goal2'

class cancel(State):
    def __init__(self):
        State.__init__(self,outcomes=['goal1','goal2','cancelled'], input_keys=['input'])

    def execute(self, ud):
        sleep(1)
        patrol.ud.inpt=int(input("enter a goal:"))
        if ud.input==1:
            return 'goal2'
        elif ud.input==2:
            return 'goal1'
       
       


class up(State):
      
        def __init__(self):
            State.__init__(self,outcomes=['up','down'])
        def execute(self, ud):
                sleep(0.5)
                rospy.wait_for_service('add_two_ints')
                try:
                    s=rospy.ServiceProxy('add_two_ints',Addtwoints)
                    res=s(1)
                    print(res)
            
                except rospy.ServiceException as e:
                    print("service call failed: %s"%e)
   

                return 'up'
    


class down(State):
      
        def __init__(self):
            State.__init__(self,outcomes=['up','down'])
        
        def execute(self, ud):
            sleep(0.5)
            rospy.wait_for_service('add_two_ints')
            try:
                s=rospy.ServiceProxy('add_two_ints',Addtwoints)
                res=s(3)
                print(res)
          
            except rospy.ServiceException as e:
                print("service call failed: %s"%e)
            return 'down'
    

class pick(State):
    def __init__(self):
        State.__init__(self,outcomes=['done','ok'])


    def execute(self, ud):
        sleep(0.5)
        rospy.wait_for_service('add_two_ints')
        try:
            s=rospy.ServiceProxy('add_two_ints',Addtwoints)
            res=s(2)
            print(res)
         
        except rospy.ServiceException as e:
            print("service call failed: %s"%e)
        # sleep(10)
        return 'pick'
    

class drop(State):
    def __init__(self):
        State.__init__(self,outcomes=['done','ok'])


    def execute(self, ud):
        sleep(0.5)
        rospy.wait_for_service('add_two_ints')
        try:
            s=rospy.ServiceProxy('add_two_ints',Addtwoints)
            res=s(4)
            print(res)
           
        except rospy.ServiceException as e:
            print("service call failed: %s"%e)
        # sleep(10)
        return 'drop'
          
def paused():
    pub_cancel_goal = rospy.Publisher('move_base/cancel',GoalID,queue_size=1) 
    count=0
    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        pub_cancel_goal.publish()
        count+=1
        if count>=5:
            break      

if __name__ == '__main__':
    rospy.init_node('patrol')
    patrol = StateMachine(['done','ok'])
    
    with patrol:
        print("state execution")
        StateMachine.add('ONE', waypoint(waypoints[0][0],waypoints[0][1]), transitions={'goal1':'UP','goal2':'DOWN','cancelled':'CANCEL'})
        StateMachine.add('UP', up(), transitions={'up':'PICK'})
        StateMachine.add('PICK', pick(), transitions={'pick':'TWO'})
        StateMachine.add('TWO', waypoint1(waypoints[1][0],waypoints[1][1]), transitions={'goal2':'DOWN','goal1':'UP','cancelled':'CANCEL'})
        StateMachine.add('DOWN', down(), transitions={'down':'DROP'})
        StateMachine.add('DROP', drop(), transitions={'drop':'ONE'})
        StateMachine.add('CANCEL', cancel(), transitions={'goal1':'UP','goal2':'DOWN','cancelled':'CANCEL'})
    sa=smach_ros.IntrospectionServer('s_server',patrol,'/SM_ROOT')
    sa.start()
    patrol.execute()
    rospy.spin()
    sa.stop()
  
        