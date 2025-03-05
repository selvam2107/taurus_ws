#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import redis
import actionlib
from hw_t.msg import aruco_detectAction, aruco_detectFeedback, aruco_detectResult
red=redis.Redis(host='192.168.5.7',port=6379)
import time
import move2
class motoraction:
    def __init__(self):
        self.return_back = False
        self.detecting = False
        self.goal = None
        self.a_server = actionlib.SimpleActionServer(
            "conveyor_pick", aruco_detectAction, execute_cb=self.execute_cb, auto_start=False)
        self.a_server.start()
        print("feirh")
    def execute_cb(self, goal):
        self.goal = goal  # Set the goal attribute
        self.feedback = aruco_detectFeedback()
        self.result = aruco_detectResult()
        self.detecting = True  # Start detecting when a goal is received
        print("cwhbug")
        red.set('pick','dsh')
        move2.write1()
        # print(red.get('pick'))
        move2.startJog()
        red.set('conveyor','forward')
        # self.detecting = False
        while not rospy.is_shutdown() and self.detecting:
            print("dwhb")
            if red.get('pick')==b'done':
                self.detecting=False
                move2.stopJog()
          

            # Detection logic is handled in the callback
            rospy.sleep(0.1)

        if self.detecting:
            self.result.distance_reached = "pick/drop completed"
            self.a_server.set_succeeded(self.result)
        elif self.a_server.is_active():
            self.result.distance_reached = "pick/drop aborted"
            self.a_server.set_aborted(self.result)
if __name__ == '__main__':
    rospy.init_node("conveyor", anonymous=True)
    red = redis.Redis(host='192.168.5.7', port='6379')

    # calib_data_path = "/home/ssapl/testbot1_ws/src/hw_t/calib_data/MultiMatrix.npz"
    # # marker_size = 6.5  # centimeters
    # camera_topic = "/scan"
    # cmd_vel_topic = "/robot/cmd_vel"

    aruco_detector = motoraction()
    
    rospy.Rate(100)
    rospy.spin()