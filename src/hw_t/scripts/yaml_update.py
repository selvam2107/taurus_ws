#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Polygon, Point32

def update_and_publish_footprint():
    rospy.init_node('update_footprint', anonymous=True)
    
    footprint_pub = rospy.Publisher('/move_base/local_costmap/footprint', Polygon, queue_size=10)
    rospy.loginfo("Footprint Publisher initialized.")
    
    updated_footprint = [[-0.105, -0.105], [-0.105, 0.105], [200, 0.105], [0.041, -0.105]]
    
    rospy.set_param('/robot_config/footprint', updated_footprint)
    rospy.loginfo(f"Updated footprint set in parameter server: {updated_footprint}")
    
    footprint_msg = Polygon()
    
    for point in updated_footprint:
        pt = Point32()
        pt.x, pt.y = point
        pt.z = 0  
        footprint_msg.points.append(pt)
    
    rate = rospy.Rate(1)  
    while not rospy.is_shutdown():
        footprint_pub.publish(footprint_msg)
        rospy.loginfo("Published updated footprint to /move_base/local_costmap/footprint")
        rate.sleep()

if __name__ == "__main__":
    try:
        update_and_publish_footprint()
    except rospy.ROSInterruptException:
        rospy.loginfo("Footprint update and publishing interrupted.")

