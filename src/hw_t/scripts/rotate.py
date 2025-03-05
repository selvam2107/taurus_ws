#!/usr/bin/env python

import rospy
import numpy as np
# import tf
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String
# Initialize ROS node
rospy.init_node("controller_node")
import redis
import time
import math
red= redis.Redis(host= '192.168.5.11',port= '6379')
# Load Parameters
# listener_dock = tf.TransformListener()
min_v = rospy.get_param("~min_v", 0.1)
min_w = rospy.get_param("~min_w", 0.1)
max_v = rospy.get_param("~max_v", 0.3)
max_w = rospy.get_param("~max_w", 0.3)
pub = rospy.Publisher("robot/cmd_vel", Twist, queue_size=20)
twist=Twist()
current_yaw=0
def odom_callback1(target_yaw):
    global pub,current_yaw
    tolerance = 0.01  # Radians, adjust as needed
    while True:
        try:
            # if red.get('rotate')==b'go':
                Kp=0.5
                # (trans_odom, rot_odom) = listener_dock.lookupTransform("map", "base_link", rospy.Time(0))

                # quaternion = [rot_odom[0], rot_odom[1], rot_odom[2], rot_odom[3]]
                # (roll, pitch, current_yaw) = tf.transformations.euler_from_quaternion(quaternion)
                sub = rospy.Subscriber('/mcl_pose',PoseStamped, odom_callback)
                yaw_error = target_yaw - current_yaw
                yaw_error = (yaw_error + np.pi) % (2 * np.pi) - np.pi
                print(current_yaw,"fdiuweh")
                if abs(yaw_error) < tolerance:
                    rospy.loginfo("Yaw aligned. Error: {:.2f} radians".format(yaw_error))
                    
                    twist.angular.z=0.0
                    time.sleep(2)
                    pub.publish(twist)
                    red.set('srotate','wed')
                    red.set('srotate1','wed')
                    red.set('srotate3','wed')
                    red.set('sgrot',"2uyg")
                    red.set('sgrot2',"2uyg")
                    return True

                angular_z = np.clip(Kp * yaw_error, -max_w, max_w)
                vel = Twist()
                vel.angular.z = angular_z
                pub.publish(vel)
                

        except Exception as e:
            # rospy.logwarn("TF lookup failed. Cannot align yaw.")
            print(e)
            # return False
# odom_callback1(-0.86) #2.28 -0.86 -2.32
def odom_callback(msg):
    global current_yaw
    odom=msg
    
    quaternion = [odom.pose.orientation.x, odom.pose.orientation.y, odom.pose.orientation.z, odom.pose.orientation.w]
    current_yaw= quaternion_to_euler(odom.pose.orientation.x, odom.pose.orientation.y, odom.pose.orientation.z, odom.pose.orientation.w)
    # current_yaw=current_yaw1
def quaternion_to_euler(x, y, z, w):
    """
    Convert a quaternion into Euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return yaw_z 
while True:
    if red.get('srotate')==b'go':
        time.sleep(5)
        odom_callback1(-0.38)
    elif red.get('srotate1')==b'go':
        time.sleep(5)
        odom_callback1(2.75)
    elif red.get('srotate3')==b'go':
        odom_callback1(2.75)
        
    elif red.get('sgrot2')==b'go':
       
        quaternion = [float(red.get('x2')), float(red.get('y2')), float(red.get('z1')), float(red.get('w1'))]
        (roll, pitch, current_yaw) = tf.transformations.euler_from_quaternion(quaternion)
        odom_callback1(current_yaw)