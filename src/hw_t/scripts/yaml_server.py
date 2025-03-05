#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Polygon, Point32
from std_msgs.msg import String

rospy.init_node('footprint_server', anonymous=True)

footprint_pub = rospy.Publisher('/move_base/local_costmap/footprint', Polygon, queue_size=10)
rospy.loginfo("Footprint Publisher initialized.")

def update_and_publish_footprint(updated_footprint):
    rospy.set_param('/robot_config/footprint', updated_footprint)
    rospy.loginfo(f"Updated footprint set in parameter server: {updated_footprint}")

    footprint_msg = Polygon()
    for point in updated_footprint:
        pt = Point32()
        pt.x, pt.y = point
        pt.z = 0  
        footprint_msg.points.append(pt)

    footprint_pub.publish(footprint_msg)
    rospy.loginfo("Published updated footprint to /move_base/local_costmap/footprint")

def footprint_request_callback(msg):
    rospy.loginfo(f"Received footprint update request: {msg.data}")
    try:
        updated_footprint = eval(msg.data)  
        update_and_publish_footprint(updated_footprint)
    except Exception as e:
        rospy.logwarn(f"Failed to update footprint: {e}")

footprint_request_sub = rospy.Subscriber('/footprint_update_request', String, footprint_request_callback)

rospy.spin()

