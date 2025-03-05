#!/usr/bin/env python3

import rospy
import time
# Brings in the SimpleActionClient
import actionlib
import redis
import time

from time import sleep
import actionlib
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from actionlib_msgs.msg import GoalID,GoalStatusArray
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
red= redis.Redis(host= '192.168.5.9',port= '6379')



def donecb(goalstatus,result):
	global done
	#print("done callback")
	print("goal status: ",goalstatus)
	#print("result:", result)

	done= True

def movebase_client(x):

	global done,prev_goal
	done= False
	red.set("key7", "junk")
	# Create an action client called "move_base" with action definition file "MoveBaseAction"
	client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

	# Waits until the action server has started up and started listening for goals.
	client.wait_for_server()

	# Creates a new goal with the MoveBaseGoal constructor
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = "map"
	goal.target_pose.header.stamp = rospy.Time.now()
	l2=[1,2]
	l3=[3,4]
	if prev_goal!=0 and x==1 and prev_goal!=1:
		l4=[16,4,5,2,14,x]
		s=4
		print('sendin way 1')
	elif prev_goal==1 and x==1:
		l4=[1]

	elif prev_goal!=0 and x==2 and prev_goal!=2:
		l4=[14,15,2,5,4,16,11]
		print('sendin way 2')
		s=4
	elif prev_goal==2 and x==2:
		l4=[11]
	elif x==2:
		l4=[11]
	else:
		l4=[x]
		s=0
	count=0
	s=0
	for p in l4:

		file= open(r"/home/taurus1/testbot_ws/src/hw_t/goals/goal_"+str(p)+".txt", "r")

		for i in range(0,8):
			file.readline()
		goal.target_pose.pose.position.x= float(file.readline()[7:-1])
		goal.target_pose.pose.position.y= float(file.readline()[7:-1])
		for i in range(0,4):
			file.readline()
		goal.target_pose.pose.orientation.z= float(file.readline()[7:-1])
		goal.target_pose.pose.orientation.w= float(file.readline()[7:-1])
		file.close()
		print("wdg")
		print(p)
		# input()
		print("x= ",goal.target_pose.pose.position.x, "y= ", goal.target_pose.pose.position.y)
		print("z= ",goal.target_pose.pose.orientation.z, "w= ", goal.target_pose.pose.orientation.w)
		if s==2 or s==1:
			time.sleep(3)
			count+=1
			if count==2:
				time.sleep(5)
				client.send_goal(goal, done_cb=donecb )
			

			client.send_goal(goal, done_cb=donecb )
		else:
			client.send_goal(goal, done_cb=donecb )
		
		# Sends the goal to the action server.
		    
		#client.cancel_goal()
		client.wait_for_result()
		if red.get('cancelg')==b'true':
			print('workings')
			while red.get('key5')!=b'5':
				pass
			red.set('key5','0')
			red.set('cancelg','false')
			client.send_goal(goal, done_cb=donecb )
			
			client.wait_for_result()
			
	while not done:
			if (red.get("key7") == b'7'):
			
				pub_cancel_goal = rospy.Publisher('move_base/cancel', GoalID, queue_size=1)
				# rospy.init_node('simp', anonymous=True)
				count = 0
				print("wdn3")
				rate = rospy.Rate(10) # 10hz
				while not rospy.is_shutdown():
					pub_cancel_goal.publish()

					count+=1
					if count >= 5:
						print("sdf")
						# input("enter something  2 send next goal")
						while red.get('key6')!=b'6':
							pass
						

						red.set('key5','false')
						break
					
					rate.sleep()
	
	# Waits for the server to finish performing the action.
	#wait = client.wait_for_result()
	# If the result doesn't arrive, assume the Server is not available
	#if not wait:
		#rospy.logerr("Action server not available!")
		#rospy.signal_shutdown("Action server not available!")
	#else:
	# Result of executing the action
	return client.get_result()   
# 'http://192.168.0.222:3001/'
# If the python node is executed as main process (sourced directly)
l=[]
prev_goal=0
while not rospy.is_shutdown():
	d={}
	l2=[]
	l=[]
	a1=str(red.get('key1'))
	a2=str(red.get('key2'))
	a3=str(red.get('key3'))
	a4=str(red.get('key4'))
	a1=int(a1[1:][1:-1])
	a2=int(a2[1:][1:-1])
	a3=int(a3[1:][1:-1])
	a4=int(a4[1:][1:-1])
	t1=str(red.get('key1t'))
	t2=str(red.get('key2t'))
	t3=str(red.get('key3t'))
	t4=str(red.get('key4t'))
	print(t1[1:][1:-1])
	t1=int(t1[1:][1:-1])
	t2=int(t2[1:][1:-1])
	t3=int(t3[1:][1:-1])
	t4=int(t4[1:][1:-1])

	# l2.append(t1)
	# l2.append(t2)
	# l2.append(t3)
	# l2.append(t4)
	# l2.sort()
	# 	for j in d:
	# 		if d[j]==i:
	# 			l.append(j)
	
	# if a1!=0 and type(a1)== int:
	# 	l.append(a1)
	# 	red.set('key1','0')
	# if a2!=0 and type(a2)== int:
	# 	l.append(a2)
	# 	red.set('key2','0')
	# if a3!=0 and type(a3)== int:
	# 	l.append(a3)
	# 	red.set('key3','0')
	# if a4!=0 and type(a4)== int:
	# 	l.append(a4)
	# 	red.set('key4','0')
	# d[1]=1
	if t1!=0 and type(t1)==int and a1!=0 and type(a1)== int:
		l2.append(t1)
		d[a1]=t1
		red.set('key1t','0')
		red.set('key1','0')
	if t2!=0 and type(t2)==int and (a2!=0 and type(a2)== int):
		l2.append(t2)
		d[a2]=t2
		red.set('key2t','0')
		red.set('key2','0')
	# if t3!=0 and type(t3)==int and (a3!=0 and type(a3)== int):
	# 	l2.append(t3)
	# 	d[a3]=t3
	# 	red.set('key3t','0')
	# 	red.set('key3','0')
	# if t4!=0 and type(t4)==int and (a4!=0 and type(a4)== int):

	# 	l2.append(t4)
	# 	d[a4]=t4
	# 	red.set('key4t','0')
	# 	red.set('key4','0')
	# print(d)
	l2.sort()
	# print(l2)
	for i in l2:
		for j in d:
			if d[j]==i:
				l.append(j)
	# print(l)
	# input()
	
	for i in l:
		#time.sleep(5)
		# input()
		print(prev_goal)
		print(i)
		while red.get('key6')!=b'6':
			pass
		red.set('key6','0')
		# input() 0.0157092553237
		# time.sleep(5)
		inpt=i
		if __name__ == '__main__':
			try:
				# Initializes a rospy node to let the SimpleActionClient publish and subscribe
				rospy.init_node('movebase_client_sequence')
					#print("while True")
				goal= inpt
				
				print("goal: ", goal)
				result = movebase_client(goal)
				print("Goal ", goal, "execution done!")
				prev_goal=goal
				print("tata! bye bye! Good bye")

				print(l)
				# input()
			except rospy.ROSInterruptException:
				rospy.loginfo("Navigation test finished.")
