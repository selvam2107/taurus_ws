#!/usr/bin/env python

import rospy
from math import pi, sqrt, fabs, atan2
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path
import tf
from tf.transformations import euler_from_quaternion
import redis
red=redis.Redis(host='localhost',port=6379)
class Task:
    def __init__(self):
        rospy.init_node('go_to_goal', anonymous=False)
        rospy.on_shutdown(self.shutdown)

        self.kp_linear = 0.3
        self.kd_linear = 0.2
        self.ki_linear = 0.0
        self.kp_angular = 0.3
        self.kd_angular = 0.1
        self.ki_angular = 0.0

        self.path = []
        self.current_waypoint = 0

        self.last_err_linear = 0
        self.integral_err_linear = 0
        self.last_err_angular = 0
        self.integral_err_angular = 0

        self.path_sub = rospy.Subscriber('/path', Path, self.path_callback)
        self.cmd_vel = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
        
        self.listener = tf.TransformListener()

    def path_callback(self, msg):
        distance=red.get('distance')
        distance=int(distance)
        print(distance,type(distance))
        if 500<=distance<=550:
                self.shutdown()
            
        self.path = [(pose.pose.position.x, pose.pose.position.y) for pose in msg.poses]
        self.path = [self.path[1],self.path[-30],self.path[-15],self.path[-1]]
        # self.path.reverse()
        
        rospy.loginfo("Path received: {} waypoints".format(len(self.path)))

    def get_distance(self, x1, y1, x2, y2):
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def get_angle(self, x1, y1, x2, y2):
        return atan2(y2 - y1, x2 - x1)

    def pid_control(self, error, last_error, integral_error, kp, kd, ki):
        integral_error += error
        derivative_error = error - last_error
        output = kp * error + kd * derivative_error + ki * integral_error
        return output, error, integral_error

    def align_to_goal(self, goal_x, goal_y):
        rate = rospy.Rate(100)
        distance=red.get('distance')
        distance=int(distance)
        print(distance,type(distance))
        while not rospy.is_shutdown() :
            current_x, current_y, current_yaw = self.get_current_pose()
            if current_x is None:
                rate.sleep()
                continue

            goal_yaw = self.get_angle(current_x, current_y, goal_x, goal_y)
            yaw_error = goal_yaw - current_yaw
            yaw_error = (yaw_error + pi) % (2 * pi) - pi  # Normalize angle

            if fabs(yaw_error) < 0.06:  # If aligned
                break

            angular_velocity, self.last_err_angular, self.integral_err_angular = self.pid_control(
                yaw_error, self.last_err_angular, self.integral_err_angular,
                self.kp_angular, self.kd_angular, self.ki_angular
            )

            twist = Twist()
            twist.angular.z = angular_velocity
            self.cmd_vel.publish(twist)
            rate.sleep()

        self.cmd_vel.publish(Twist())  # Stop rotation
    def move_to_waypoint(self, goal_x, goal_y):
        rate = rospy.Rate(200)
        distance=red.get('distance')
        distance=int(distance)
        print(distance,type(distance))
        while not rospy.is_shutdown() :
            current_x, current_y, current_yaw = self.get_current_pose()
            if current_x is None:
                rate.sleep()
                continue

            distance_error = self.get_distance(current_x, current_y, goal_x, goal_y)
            goal_yaw = self.get_angle(current_x, current_y, goal_x, goal_y)
            yaw_error = goal_yaw - current_yaw
            yaw_error = (yaw_error + pi) % (2 * pi) - pi  # Normalize angle

            if distance_error < 0.1:  # If close enough to the waypoint
                break

            linear_velocity, self.last_err_linear, self.integral_err_linear = self.pid_control(
                distance_error, self.last_err_linear, self.integral_err_linear,
                self.kp_linear, self.kd_linear, self.ki_linear
            )
            angular_velocity, self.last_err_angular, self.integral_err_angular = self.pid_control(
                yaw_error, self.last_err_angular, self.integral_err_angular,
                self.kp_angular, self.kd_angular, self.ki_angular
            )

            twist = Twist()
            twist.linear.x = min(linear_velocity, 0.2)
            twist.angular.z = angular_velocity
            self.cmd_vel.publish(twist)
            rate.sleep()

        self.cmd_vel.publish(Twist())  # Stop forward motion

    def get_current_pose(self):
        try:
            (trans, rot) = self.listener.lookupTransform('map', 'base_link', rospy.Time(0))
            roll, pitch, yaw = euler_from_quaternion(rot)
            return trans[0], trans[1], yaw
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logwarn("TF lookup failed")
            return None, None, None

    def move(self):
        rate = rospy.Rate(100)
        while not rospy.is_shutdown() and self.current_waypoint < len(self.path):
            
            goal_x, goal_y = self.path[self.current_waypoint]
            self.align_to_goal(goal_x, goal_y)
            self.move_to_waypoint(goal_x, goal_y)
            self.current_waypoint += 1
            rate.sleep()

    def shutdown(self):
        twist=Twist()
        rospy.loginfo("Stopping the robot...")
        twist.linear.x=0
        twist.angular.z=0
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    Task = Task()
    rospy.sleep(1)
    Task.move()
