#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import redis
import actionlib
from geometry_msgs.msg import PoseWithCovarianceStamped
from datetime import datetime
from hw_t.msg import aruco_detectAction, aruco_detectFeedback, aruco_detectResult
import math
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import tf
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
red = redis.Redis(host='localhost', port=6379)
from actionlib_msgs.msg import GoalID


class MotorAction:
	def __init__(self):
		self.return_back = False
		self.detecting = False
		self.goal = None
		self.initial_pose = None
		
        
		self.a_server = actionlib.SimpleActionServer(
            "Table_path", aruco_detectAction, execute_cb=self.execute_cb, auto_start=False)
		self.a_server.start()
		print("Action server started")


	def execute_cb(self, goal):
		rospy.set_param('/navigation',4)
		self.goal = goal
		self.feedback = aruco_detectFeedback()
		self.result = aruco_detectResult()
		self.detecting = True
		
		while not rospy.is_shutdown() and self.detecting:
				yaw = 0
				x=int(input('enter goal number'))
				file= open(r"/root/testbot_ws/src/hw_t/goals/goal_"+str(x)+".txt", "r")

				for i in range(0,8):
					file.readline()
				x= float(file.readline()[7:-1])
				y= float(file.readline()[7:-1])
				for i in range(0,4):
					file.readline()
				z= float(file.readline()[7:-1])
				w= float(file.readline()[7:-1])
				file.close()

				# Get the orientation and normalize it
				quaternion = 0
				if quaternion is None:
					rospy.logerr("Invalid quaternion, cannot proceed with goal.")
					return

				(trans_odom, rot_odom) = listener_dock.lookupTransform("map", "base_link", rospy.Time(0))
				(roll, pitch, current_yaw) = tf.transformations.euler_from_quaternion([0,0,z,w])
				print(current_yaw, "yaw")
				
				if current_yaw <= 0:
					yaw = current_yaw+ 3.141592653589793
				else:
					yaw = current_yaw - 3.141592653589793

				rospy.loginfo("Goal Position: x=")
				# point = (goal_x, goal_y, 0,goal_w,goal_z)
				# a = talker()
				# while not a:
				#     pass
				point = (x, y, 0,w,z)
				# create_orientation_line(point,yaw, w,z)

				def talker():
					pub_cancel_goal = rospy.Publisher('move_base/cancel', GoalID, queue_size=1)
					goal_id = GoalID()
					goal_id.stamp = rospy.Time.now()  # optional
					pub_cancel_goal.publish(goal_id)
					# pub_cancel_goal = rospy.Publisher('move_base/cancel', GoalID, queue_size=1)
					count = 0
					rate = rospy.Rate(10)  # 10hz
					while not rospy.is_shutdown():
						pub_cancel_goal.publish()
						count += 1
						if count >= 5:
							return True
							rate.sleep()
				a = talker()

				def create_orientation_line(point, yaw, goal_w,goal_z,length=3.0, num_points=100,):
					path_pub = rospy.Publisher('/path', Path, queue_size=10)
					path = Path()
					path.header.frame_id = "map"

					poin_list = []
					x_start, y_start, z_start ,a,s= point
					for i in range(num_points):
						t = i / float(num_points)
						x = x_start + t * length * math.cos(yaw)
						y = y_start + t * length * math.sin(yaw)
						z = z_start
						l = (x, y, z)
						pose = PoseStamped()
						pose.header.frame_id = "map"
						pose.pose.position.x = x
						pose.pose.position.y = y
						pose.pose.position.z = z
						pose.pose.orientation.w = -yaw  # Set a default orientation (no rotation)
						path.poses.append(pose)
						poin_list.append(l)
					print(poin_list)

					client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
					client.wait_for_server()

					goal = MoveBaseGoal()
					goal.target_pose.header.frame_id = "map"
					goal.target_pose.header.stamp = rospy.Time.now()
					goal.target_pose.pose.position.x = poin_list[-1][0]
					goal.target_pose.pose.position.y = poin_list[-1][1]
					goal.target_pose.pose.orientation.x = 0
					goal.target_pose.pose.orientation.y = 0
					goal.target_pose.pose.orientation.w = goal_w 
					goal.target_pose.pose.orientation.z=goal_z # Set a default orientation (no rotation)
					
					client.send_goal(goal)
					rospy.loginfo("Sent goal to move_base:")
					s=client.wait_for_result()
					print("")
					red.set('dock','go')
					rate = rospy.Rate(10)
					# talker()
					r = rospy.get_param("path_done")
					print(r)
					while r==1:
						r = rospy.get_param("path_done")
						path.header.stamp = rospy.Time.now()
						path_pub.publish(path)
						rate.sleep()
						print('sdjhb')
					else:
						self.detecting=False
				create_orientation_line(point,yaw, w,z)

if __name__ == '__main__':
    rospy.init_node("conveyor", anonymous=True)
    red = redis.Redis(host='localhost', port=6379)
    listener_dock = tf.TransformListener()
    aruco_detector = MotorAction()
    rospy.spin()
    