#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Pose2D
from nav_msgs.msg import Path
import math
from geometry_msgs.msg import PoseStamped
import redis
red= redis.Redis(host= 'localhost',port= '6379')
class PoseSubscriber:
    def __init__(self):
        rospy.init_node('pose_subscriber', anonymous=False)
        rospy.on_shutdown(self.shutdown)
        
        # Subscriber to the /pos_angle topic
        self.pose_sub = rospy.Subscriber('/v_plate_pose_in_map', PoseStamped, self.pose_callback)
        self.current_pose = Pose2D()

    def pose_callback(self, msg):
        # Store the received pose
        self.current_pose = msg
        rospy.loginfo(f"Received Pose - X: {self.current_pose.pose.position.x}, Y: {self.current_pose.pose.position.y}, Theta: {self.current_pose.pose.orientation.w}")
        point=(2.0930161476135254,-1.2350019216537476,0)
        # yaw=(self.current_pose.pose.orientation.w*-1)+3.142
        self.create_orientation_line(point,1.567,2)
    def create_orientation_line(self,point, yaw, length,num_points=100):
        path_pub = rospy.Publisher('/path', Path, queue_size=10)
        path = Path()
        path.header.frame_id = "map"
        count=0
        poin_list = []
        x_start, y_start, z_start = point
        for i in range(num_points):
            t = i / float(num_points)
            x = x_start + t * length * math.cos(-yaw)
            y = y_start + t * length * math.sin(-yaw)
            z = z_start
            l = (x, y, z)
            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.position.z = z
            pose.pose.orientation.w = yaw  # Set a default orientation (no rotation)
            count+=1
            if count>=50:
                path.poses.append(pose)
            poin_list.append(l)
        print(poin_list)

        # print(len(path))
        rate = rospy.Rate(10)
        while red.get("v_dock")!=b"success":
            path.header.stamp = rospy.Time.now()
            path_pub.publish(path)
            rate.sleep()
           

            
            # Additional processing can be done here using self.current_pose
        
    def shutdown(self):
        rospy.loginfo("Shutting down the Pose Subscriber Node.")

if __name__ == '__main__':
    try:
        pose_subscriber = PoseSubscriber()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
