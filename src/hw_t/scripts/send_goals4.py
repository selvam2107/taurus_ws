#!/usr/bin/env python3.6

import rospy
import time
# Brings in the SimpleActionClient
import actionlib
import redis
import time
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
red= redis.Redis(host= 'localhost',port= '6379')



def donecb(goalstatus,result):
	global done
	#print("done callback")
	print("goal status: ",goalstatus)
	#print("result:", result)

	done= True

def movebase_client(x):

	global done
	done= False
	red.set("goal", "junk")
	# Create an action client called "move_base" with action definition file "MoveBaseAction"
	client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

	# Waits until the action server has started up and started listening for goals.
	client.wait_for_server()

	# Creates a new goal with the MoveBaseGoal constructor
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = "map"
	goal.target_pose.header.stamp = rospy.Time.now()


	file= open(r"/root/testbot_ws/src/hw_t/goals/goal_"+str(x)+".txt", "r")

	for i in range(0,8):
		file.readline()
	goal.target_pose.pose.position.x= float(file.readline()[7:-1])
	goal.target_pose.pose.position.y= float(file.readline()[7:-1])
	for i in range(0,4):
		file.readline()
	goal.target_pose.pose.orientation.z= float(file.readline()[7:-1])
	goal.target_pose.pose.orientation.w= float(file.readline()[7:-1])
	file.close()


	print("x= ",goal.target_pose.pose.position.x, "y= ", goal.target_pose.pose.position.y)
	print("z= ",goal.target_pose.pose.orientation.z, "w= ", goal.target_pose.pose.orientation.w)

	# Sends the goal to the action server.
	client.send_goal(goal, done_cb=donecb )
	#client.cancel_goal()

	while not done:
		if (red.get("goal") == b'cancel'):
		
			client.cancel_goal()
			input("enter somthing to send next goal")
			red.set("goal", "junk")
			break

	# Waits for the server to finish performing the action.
	#wait = client.wait_for_result()
	# If the result doesn't arrive, assume the Server is not available
	#if not wait:
		#rospy.logerr("Action server not available!")
		#rospy.signal_shutdown("Action server not available!")
	#else:
	# Result of executing the action
	return client.get_result()   

# If the python node is executed as main process (sourced directly)
l=[1,2,3]
while not rospy.is_shutdown():
	
	# input()
	for i in l:
		print(i)
		# if i !=3:
		# time.sleep(10)
			# input()
		# else:
		# 	pass
	
		# input()
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

				print("tata! bye bye! Good bye")


			except rospy.ROSInterruptException:
				rospy.loginfo("Navigation test finished.")
