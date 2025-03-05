#!/usr/bin/env python
import cv2 as cv
import os
from cv2 import aruco
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import rospy
import actionlib
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import time
import redis
from hw_t.msg import aruco_detectAction, aruco_detectFeedback, aruco_detectResult,aruco_detectGoal
red=redis.Redis(host='localhost',port=6379)
class ArucoDetector:
    def __init__(self, calib_data_path, marker_size, camera_topic, cmd_vel_topic):
        # Load calibration data
        self.calib_data = np.load(calib_data_path)
        self.cam_mat = self.calib_data["camMatrix"]
        self.dist_coef = self.calib_data["distCoef"]
        self.MARKER_SIZE = marker_size

        # Initialize ArUco marker dictionary and parameters
        self.marker_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.param_markers = aruco.DetectorParameters_create()

        self.return_back = False
        self.detecting = False
        self.goal = None


        # Initialize CvBridge for converting ROS Image messages to OpenCV images
        self.bridge = CvBridge()
        self.twist = Twist()

        # Setup publishers and subscribers
        self.cmd_vel_pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=1)
        rospy.Subscriber(camera_topic, Image, self.callback_fun)

        # Setup action server
        self.a_server = actionlib.SimpleActionServer(
            "ArucoDetection", aruco_detectAction, execute_cb=self.execute_cb, auto_start=False)
        self.a_server.start()
        # self.execute_cb(1)
    def execute_cb(self, goal):
        self.goal = goal  # Set the goal attribute
        self.feedback = aruco_detectFeedback()
        self.result = aruco_detectResult()
        self.detecting = True  # Start detecting when a goal is received

        while not rospy.is_shutdown() and self.detecting:
            if self.a_server.is_preempt_requested():
                rospy.loginfo('Preempted ArucoDetection')
                self.a_server.set_preempted()
                self.detecting = False
                print("edhgduy2u")
                return

            # Detection logic is handled in the callback
            rospy.sleep(0.1)

        if self.detecting:
            # a=self.back()
            # if a:
                
            self.result.distance_reached = "Detection completed"
            self.a_server.set_succeeded(self.result)
        # elif self.a_server.is_active():
        #     self.result.distance_reached = "Detection aborted"
        #     self.a_server.set_aborted(self.result)

    def callback_fun(self, msg):
        if not self.detecting:
            return  # Exit callback if not in detecting mode
        try:
            # Convert ROS image message to OpenCV image
            cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            h, w = cv_img.shape[:2]
            mid_x = w / 2

            # Process the image to detect ArUco markers
            gray_frame = cv.cvtColor(cv_img, cv.COLOR_BGR2GRAY)
            marker_corners, marker_IDs, _ = aruco.detectMarkers(gray_frame, self.marker_dict, parameters=self.param_markers)

            if marker_corners:
                rVec, tVec, _ = aruco.estimatePoseSingleMarkers(marker_corners, self.MARKER_SIZE, self.cam_mat, self.dist_coef)
                for ids, corners, i in zip(marker_IDs, marker_corners, range(marker_IDs.size)):
                    cv.polylines(cv_img, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA)
                    corners = corners.reshape(4, 2).astype(int)

                    # Calculate the distance to the marker
                    # distance = np.linalg.norm(tVec[i][0])
                    # print("Distance to marker",distance)

                    # Draw the pose of the marker
                    aruco.drawAxis(cv_img, self.cam_mat, self.dist_coef, rVec[i], tVec[i], 4)

                    mid_point1 = int((corners[0][0] + corners[2][0]) / 2)
                    mid_point2 = int((corners[0][1] + corners[2][1]) / 2)

                    cv.circle(cv_img, (320, 240), 5, (0, 0, 0), -1)
                    cv.circle(cv_img, (mid_point1, mid_point2), 5, (0, 0, 0), -1)

                    if self.goal.detect == 1:
                        print("Detecting ArUco marker")
                        self.feedback.reached = "reaching"
                        # self.a_server.publish_feedback(self.feedback)
                        distance=red.get('distance')
                        distance=int(distance)
                        print(distance,type(distance))
                        if distance > 0 :
                            if 175<=distance<=210:
                                self.twist.linear.x = 0
                                self.twist.angular.z = 0
                                self.cmd_vel_pub.publish(self.twist)
                                time.sleep(5)
                                while distance<=1250.00:
                                    print(distance)
                                    distance=red.get('distance')
                                    distance=int(distance)
                                    self.twist.linear.x = -0.2
                                    self.cmd_vel_pub.publish(self.twist)
                                self.detecting=False
                            elif (mid_point1 - 30) <= mid_x <= (mid_point1 + 30):
                                self.twist.linear.x = 0.08
                                self.twist.angular.z = 0
                                print("Going straight")
                            elif mid_x > (mid_point1 + 30):
                                self.twist.angular.z = 0.03
                                print("Turning left")
                            elif mid_x < (mid_point1 - 30):
                                self.twist.angular.z = -0.03
                                print("Turning right")
                            self.cmd_vel_pub.publish(self.twist)
                         
                        #     self.return_back = True

                        # if self.return_back:
                        #     print("Returning")
                        #     self.twist.linear.x = -0.05
                        #     self.twist.angular.z = 0
                        #     self.cmd_vel_pub.publish(self.twist)
                        #     if distance >= 150:
                        #         time.sleep(1)
                        #         self.twist.linear.x = 0
                        #         self.twist.angular.z = 0
                        #         self.cmd_vel_pub.publish(self.twist)
                        #          # self.a_server.set_succeeded(self.result)
                        #         self.return_back = False
                                # self.detecting = False  # Stop detecting after return
            else:
                self.twist.angular.z=0.0
                self.twist.linear.x = 0
                self.cmd_vel_pub.publish(self.twist)
            # cv.imshow("frame", cv_img)
            # cv.waitKey(1)
        except CvBridgeError as e:
            print("CvBridge Error:",e)
    def back(self):
        distance=red.get('distance')
        distance=int(distance)
        print("cwijbciuew")
        while distance<=1500.00:
            print(distance)
            distance=red.get('distance')
            distance=int(distance)
            self.twist.linear.x = -0.2
            self.cmd_vel_pub.publish(self.twist)
        print("ended")
        self.twist.linear.x = 0
        self.cmd_vel_pub(self.twist)
        self.result.distance_reached = "Detection completed"
        self.a_server.set_succeeded(self.result)
        return True

        



if __name__ == "__main__":
    rospy.init_node("aruco_detect", anonymous=True)
    red = redis.Redis(host='localhost', port='6379')

    calib_data_path = "/root/testbot_ws/src/hw_t/calib_data/MultiMatrix.npz"
    marker_size = 10  # centimeters
    camera_topic = "/camera/color/image_raw"
    cmd_vel_topic = "/robot/cmd_vel"

    aruco_detector = ArucoDetector(calib_data_path, marker_size, camera_topic, cmd_vel_topic)

    rospy.spin()
    cv.destroyAllWindows()
