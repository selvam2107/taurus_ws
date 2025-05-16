#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Quaternion
import numpy as np

class IMUToOdom:
    def __init__(self):
        rospy.init_node('imu_to_odom_node')

        self.odom_pub = rospy.Publisher('/imu_odom', Odometry, queue_size=10)
        rospy.Subscriber('/imu/data', Imu, self.imu_callback)

        self.odom_frame = "odom"
        self.base_frame = "base_link"

        self.last_time = None
        self.velocity = np.array([0.0, 0.0])   # vx, vy
        self.position = np.array([0.0, 0.0])   # x, y

    def imu_callback(self, imu_msg):
        current_time = imu_msg.header.stamp.to_sec()
        if self.last_time is None:
            self.last_time = current_time
            return
        
        dt = current_time - self.last_time
        self.last_time = current_time

        # Get linear acceleration (assuming flat ground)
        ax = imu_msg.linear_acceleration.x
        ay = imu_msg.linear_acceleration.y

        acc = np.array([ax, ay])

        # Update position: p = p + v*dt + 0.5*a*dt^2
        self.position += self.velocity * dt + 0.5 * acc * dt**2

        # Update velocity: v = v + a*dt
        self.velocity += acc * dt

        # Build odometry message
        odom_msg = Odometry()
        odom_msg.header.stamp = imu_msg.header.stamp
        odom_msg.header.frame_id = self.odom_frame
        odom_msg.child_frame_id = self.base_frame

        # Set pose.position (calculated)
        odom_msg.pose.pose.position.x = self.position[0]
        odom_msg.pose.pose.position.y = self.position[1]
        odom_msg.pose.pose.position.z = 0.0

        # Orientation from IMU
        odom_msg.pose.pose.orientation = imu_msg.orientation
        odom_msg.pose.covariance = list(imu_msg.orientation_covariance)

        # Velocity
        odom_msg.twist.twist.linear.x = self.velocity[0]
        odom_msg.twist.twist.linear.y = self.velocity[1]
        odom_msg.twist.twist.linear.z = 0.0
        odom_msg.twist.twist.angular = imu_msg.angular_velocity

        # Covariances (edit as needed)
        odom_msg.twist.covariance = [0.1]*36
        odom_msg.pose.covariance = [0.2]*36

        self.odom_pub.publish(odom_msg)

if __name__ == '__main__':
    try:
        IMUToOdom()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
