import rospy
import numpy as np
import tf
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String
# Initialize ROS node
rospy.init_node("controller_node2")
import redis
import time
import math
listener_dock = tf.TransformListener()
pub=rospy.Publisher("lidar_status",String,queue_size=10)
def odom_callback1():
    global pub
    # global pub,current_yaw
    # tolerance = 0.01  # Radians, adjust as needed
    
    try:
            # if red.get('rotate')==b'go':
                # Kp=0.5
                
                (trans_odom, rot_odom) = listener_dock.lookupTransform("map", "base_link", rospy.Time(0))
                print("aij")
                re="lidar is healthy"
                pub.publish(re)

    except Exception as e:
            # print("widuhu",e)
            re="lidar is not working propery please check lidar cable and ip address"
            pub.publish(re)
while not rospy.is_shutdown():
    odom_callback1()