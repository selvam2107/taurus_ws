#!/usr/bin/env python3.6

import rospy
import time
from geometry_msgs.msg import PoseWithCovarianceStamped
import redis
red= redis.Redis(host= 'localhost',port= '6379')

def callback(msg): 
	global first
	x=""

	
	print(msg)
	
	
	try:
		if red.get('emg')==b"on":
			print("Header.seq=",msg.header.seq)
			file= open(r"/home/ssapl/testbot_ws/src/hw_t/goals/pose_"+".txt", "w")
			file.write(str(msg))
			file.close()

			print("saved as home/taurus/hw_t/goals/pose_",".txt")
			
		elif red.get('emg')=='off':
			if first: pass
			time.sleep(3)
			file= open(r"/home/ssapl/testbot_ws/src/hw_t/goals/pose_.txt", "r")
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
			red.set('emg','no')

		else:
			pass
	except Exception as e:
		print(e)

	print("fgbvuy")


if __name__ == '__main__':
	# Initializes a rospy node to let the SimpleActionClient publish and subscribe
	rospy.init_node('initpose')
	 
	sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, callback) #We subscribe to the laser's topic
	pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=1)
	# pose1= PoseWithCovarianceStamped()
	rate = rospy.Rate(2)
	first= True
	
	rospy.spin()
