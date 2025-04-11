#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import redis
import actionlib
from geometry_msgs.msg import PoseWithCovarianceStamped
from datetime import datetime
from hw_t.msg import aruco_detectAction, aruco_detectFeedback, aruco_detectResult
import math

red = redis.Redis(host='localhost', port=6379)

class MotorAction:
    def __init__(self):
        self.return_back = False
        self.detecting = False
        self.goal = None
        self.initial_pose = None
        self.cmd_vel_pub = rospy.Publisher("/robot/cmd_vel", Twist, queue_size=1)
        self.odom_sub = rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, self.odom_callback)
        
        self.a_server = actionlib.SimpleActionServer(
            "back", aruco_detectAction, execute_cb=self.execute_cb, auto_start=False)
        self.a_server.start()
        print("Action server started")

    def odom_callback(self, msg):
        position = msg.pose.pose.position
        self.current_pose = (position.x, position.y)
        
    def calculate_distance(self, start, end):
        return math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)

    def execute_cb(self, goal):
        self.goal = goal
        self.feedback = aruco_detectFeedback()
        self.result = aruco_detectResult()
        self.detecting = True
        red.set('conveyor', 'reverse')
        
        while not rospy.is_shutdown() and self.detecting:
            print("Detecting obstacles and moving")
            self.ip = self.current_pose
            
            while self.calculate_distance(self.ip, self.current_pose) < 1.5:
                r = rospy.get_param("/distance_goal_qr", self.goal)
                if r == 0:
                    self.a_server.set_preempted()
                    self.detecting = False
                    return
                
                rospy.Subscriber("/scan_2", LaserScan, self.callback)
                rospy.sleep(0.25)
                
                twist = Twist()
                if self.no_obstacle == 'yes':
                    twist.linear.x = 0
                else:
                    twist.linear.x = -0.1
                    self.cmd_vel_pub.publish(twist)
                
            print("Moved 1.5 meters, stopping.")
            twist.linear.x = 0
            self.cmd_vel_pub.publish(twist)
            
            self.result.distance_reached = "pick/drop completed"
            self.a_server.set_succeeded(self.result)
            self.detecting = False
            return

    def callback(self, scan_data):
        self.no_obstacle = 'no'
        for i, range_distance in enumerate(scan_data.ranges):
            angle = scan_data.angle_min + i * scan_data.angle_increment
            if -1.00 <= angle <= -0.65 and 0.05 <= range_distance <= 0.6:
                self.no_obstacle = 'yes'
                return
            if -1.65 <= angle <= -1.45 and 0.05 <= range_distance <= 1:
                self.no_obstacle = 'yes'
                return
            if 0.60 <= angle <= 0.0 and 0.05 <= range_distance <= 1:
                self.no_obstacle = 'yes'
                return
            if -2.18<=angle<=-1.65 and 0.05 <= range_distance <= 1.1:
                self.no_obstacle = 'yes'
                return

if __name__ == '__main__':
    rospy.init_node("conveyor", anonymous=True)
    red = redis.Redis(host='localhost', port=6379)
    
    aruco_detector = MotorAction()
    rospy.spin()
