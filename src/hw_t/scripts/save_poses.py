#!/usr/bin/env python3

import rospy
import time
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PoseStamped


def callback(msg): 
	#global first

	#if first:

	try:
		num= int(input("enter goal number"))
		print("Header.seq=",msg.header.seq)
		file= open(r"/root/testbot_ws/src/hw_t/goals/goal_"+str(num)+".txt", "w")
		file.write(str(msg))
		file.close()

		print("saved as home/taurus/hw_t/goals/goal_",num,".txt")
		input("enter something to get next pose")
	except:
		print("You probably entered an invalid number, enter a Valid one")


if __name__ == '__main__':
	# Initializes a rospy node to let the SimpleActionClient publish and subscribe
	rospy.init_node('initpose')
	sub = rospy.Subscriber('/move_base_simple/goal', PoseStamped, callback, queue_size=1) #We subscribe to the laser's topic
	#pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=1)
	pose1= PoseWithCovarianceStamped()
	rate = rospy.Rate(2)
	#first= True
	
	rospy.spin()
