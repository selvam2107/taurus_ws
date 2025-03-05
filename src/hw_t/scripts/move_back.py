#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import redis
import actionlib
import time
from hw_t.msg import aruco_detectAction, aruco_detectFeedback, aruco_detectResult
red=redis.Redis(host='localhost',port=6379)
rospy.init_node("back", anonymous=True)
cmd_vel_pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
twist = Twist()
while True:

    if red.get("back")==b'go':
        twist.linear.x=-0.1
        cmd_vel_pub.publish(twist)
    elif red.get("back")==b'stop':
        pass
    else:
        twist.linear.x=0
        red.set('back','stop')
        cmd_vel_pub.publish(twist)
    
        