#!/usr/bin/env python
import rospy
import tf
from geometry_msgs.msg import PoseStamped
import math

class VPlateTransform:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('v_plate_transform', anonymous=True)
        self.listener_dock = tf.TransformListener()
        
        # Get parameters
        self.map_frame = rospy.get_param('~map_frame', 'map')
        self.v_plate_frame = rospy.get_param('~v_plate_frame', 'triangle_ref')

        # Initialize a transform listener
        self.tf_listener = tf.TransformListener()

        # Publisher for the V-plate pose in the map frame
        self.pose_pub = rospy.Publisher('/v_plate_pose_in_map', PoseStamped, queue_size=10)

    def get_v_plate_transform(self):
        try:
            # Wait for the transform to become available
            self.tf_listener.waitForTransform(self.map_frame, self.v_plate_frame, rospy.Time(0), rospy.Duration(1.0))
            (trans, rot) = self.tf_listener.lookupTransform(self.map_frame, self.v_plate_frame, rospy.Time(0))
            quaternion = [0.0, 0.0 , -0.7016138813840317,  0.7125573390606779]
            (roll, pitch, current_yaw) = tf.transformations.euler_from_quaternion(quaternion)
            print(quaternion,"eqib")

            # Create a PoseStamped message #-1.46746825449
            self.pose = PoseStamped()
            self.pose.header.stamp = rospy.Time.now()
            self.pose.header.frame_id = self.map_frame

            # Set the position
            self.pose.pose.position.x = trans[0]
            self.pose.pose.position.y = trans[1]
            self.pose.pose.position.z = trans[2]
            print(trans)

            # Set the orientation
            self.pose.pose.orientation.x = rot[0]
            self.pose.pose.orientation.y = rot[1]
            self.pose.pose.orientation.z = rot[2]
            self.pose.pose.orientation.w = current_yaw

            # Publish the pose
            self.pose_pub.publish(self.pose)

            # Print the transformation details
            # rospy.loginfo("V-plate Position in Map Frame: x={}, y={}, z={}".format(trans[0], trans[1], trans[2]))
            # Wrospy.loginfo("V-plate Orientation in Map Frame (quaternion): x={}, y={}, z={}, w={}".format(rot[0], rot[1], rot[2], rot[3]))

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
            rospy.logerr("TF Exception: ")
    
    def run(self):
        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            self.get_v_plate_transform()
            rate.sleep()

if __name__ == '__main__':
    try:
        v_plate_tf = VPlateTransform()
        v_plate_tf.run()
    except :
        print("wqd")
