#!/usr/bin/env python3
import rospy
while not rospy.is_shutdown():
    rospy.set_param("navigation",1)
rospy.set_param("navigation",0)

