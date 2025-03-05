#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import String
import rospy

from time import sleep
import actionlib
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from actionlib_msgs.msg import GoalID,GoalStatusArray
import redis
red= redis.Redis(host= '192.168.5.4',port= '6379')
def talker():
   
    while True:
        if red.get('key7')==b'7':
            print('true')
            pub_cancel_goal = rospy.Publisher('move_base/cancel', GoalID, queue_size=1)
            rospy.init_node('simp', anonymous=True)
            count = 0
            
            red.set('key7','0')
            rate = rospy.Rate(10) # 10hz
            while not rospy.is_shutdown():
                pub_cancel_goal.publish()
                red.set('cancelg','true')
            # sleep(5)
            # print("executed cancel goal")
                count+=1
                if count >= 5:
                    print("sdf")
                    
                    break
                
                rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

