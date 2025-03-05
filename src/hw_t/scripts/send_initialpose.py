#!/usr/bin/env python3

import rospy
import time
from geometry_msgs.msg import PoseWithCovarianceStamped

def callback(msg): 
	global first,count
	print("wihb")
	if first and count==1:
		print("sent")
		time.sleep(3)
		file= open(r"/root/testbot_ws/src/hw_t/goals/initialpose).txt", "r")
		pose1.header.frame_id= 'map'
		for i in range(0,9):
			file.readline()
		pose1.pose.pose.position.x= float(file.readline()[9:-1])
		pose1.pose.pose.position.y= float(file.readline()[9:-1])
		for i in range(0,4):
			file.readline()
		pose1.pose.pose.orientation.z= float(file.readline()[9:-1])
		pose1.pose.pose.orientation.w= float(file.readline()[9:-1])
		# pose1.pose.covariance=  list(map(float, (file.readline()[15:-2]).split(',')))
		l=[]
		s=file.readline()[14:-1]
		s=s.split(",")
		
		for i in range(len(s)):
			
			if i==0:
				m=s[i]
				i=m[1:]
				l=l+[float(i)]
			else:
				l=l+[float(s[i])]
		print(l,"success")		
		pose1.pose.covariance=l
		file.close()
		#print(pose1)
		pub.publish(pose1)
		print("published pose")
		time.sleep(1)
		pub.publish(pose1)
		print("published pose")
		first= False
		count=0
		


	


if __name__ == '__main__':
	# Initializes a rospy node to let the SimpleActionClient publish and subscribe
	count=1
	first= True
	# while count!=0:
	rospy.init_node('initpose')
	sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, callback) #We subscribe to the laser's topic
	pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=1)
	pose1= PoseWithCovarianceStamped()
	rate = rospy.Rate(2)
		
		
	rospy.spin()
