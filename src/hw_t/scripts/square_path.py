#!/usr/bin/env python

import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import math
import tf
from actionlib_msgs.msg import GoalID
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import redis
red= redis.Redis(host= 'localhost',port= '6379')
def normalize_quaternion(quaternion):
    length = math.sqrt(quaternion.x**2 + quaternion.y**2 + quaternion.z**2 + quaternion.w**2)
    if length == 0:
        rospy.logwarn("Quaternion has zero length, cannot normalize.")
        return None
    quaternion.x /= length
    quaternion.y /= length
    quaternion.z /= length
    quaternion.w /= length
    return quaternion

def goal_callback(goal_msg):
    # Extract the goal values
    print(goal_msg)
    yaw = 0
    goal_x = goal_msg.pose.position.x
    goal_y = goal_msg.pose.position.y
    goal_w=goal_msg.pose.orientation.w
    goal_z=goal_msg.pose.orientation.z

    # Get the orientation and normalize it
    quaternion = normalize_quaternion(goal_msg.pose.orientation)
    if quaternion is None:
        rospy.logerr("Invalid quaternion, cannot proceed with goal.")
        return

    (trans_odom, rot_odom) = listener_dock.lookupTransform("map", "base_link", rospy.Time(0))
    (roll, pitch, current_yaw) = tf.transformations.euler_from_quaternion([0, 0, goal_z, goal_w])
    print(current_yaw, "yaw")
    
   

    rospy.loginfo("Goal Position: x=")
    point = (goal_x, goal_y, 0,goal_w,goal_z)
    a = talker()
    while not a:
        pass

    create_orientation_line(point, current_yaw, goal_w,goal_z)

def talker():
    pub_cancel_goal = rospy.Publisher('move_base/cancel', GoalID, queue_size=1)
    count = 0
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        pub_cancel_goal.publish()
        count += 1
        if count >= 5:
            return True
        rate.sleep()

def create_orientation_line(point, yaw, goal_w,goal_z,length=7, num_points=100,):
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
        pose.pose.orientation.w = goal_w  # Set a default orientation (no rotation)
        path.poses.append(pose)
        poin_list.append(l)
    print(poin_list)
    x,y,z=poin_list[-1]
    length=4.5
    for i in range(15):
        t = i / float(num_points)
        x = x + t * length * math.cos(yaw+1.57)
        y = y+ t * length * math.sin(yaw+1.57)
        z = z_start
        l = (x, y, z)
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z
        pose.pose.orientation.w = goal_w  # Set a default orientation (no rotation)
        path.poses.append(pose)
        poin_list.append(l)
    print(poin_list)
    x,y,z=poin_list[-1]
    length=7
    for i in range(15):
        t = i / float(num_points)
        x = x + t * length * math.cos(yaw+3.14)
        y = y+ t * length * math.sin(yaw+3.14)
        z = z_start
        l = (x, y, z)
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z
        pose.pose.orientation.w = goal_w  # Set a default orientation (no rotation)
        path.poses.append(pose)
        poin_list.append(l)
    print(poin_list)
    x,y,z=poin_list[-1]
    length=4.5
    for i in range(15):
        t = i / float(num_points)
        x = x + t * length * math.cos(yaw-1.57)
        y = y+ t * length * math.sin(yaw-1.57)
        z = z_start
        l = (x, y, z)
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z
        pose.pose.orientation.w = goal_w  # Set a default orientation (no rotation)
        path.poses.append(pose)
        poin_list.append(l)
    print(poin_list)


    # client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    # client.wait_for_server()

    # goal = MoveBaseGoal()
    # goal.target_pose.header.frame_id = "map"
    # goal.target_pose.header.stamp = rospy.Time.now()
    # goal.target_pose.pose.position.x = poin_list[-1][0]
    # goal.target_pose.pose.position.y = poin_list[-1][1]
    # goal.target_pose.pose.orientation.w = goal_w 
    # goal.target_pose.pose.orientation.z=goal_z # Set a default orientation (no rotation)
    
    # client.send_goal(goal)
    rospy.loginfo("Sent goal to move_base:")
    # client.wait_for_result()
    print("ndiwidwedhi")
    red.set('dock','go')
    rate = rospy.Rate(10)
    while True:
        path.header.stamp = rospy.Time.now()
        path_pub.publish(path)
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('orientation_line_publisher', anonymous=True)
    listener_dock = tf.TransformListener()
    rospy.Subscriber('/move_base_simple/goal', PoseStamped, goal_callback, queue_size=1)
    rospy.spin()
