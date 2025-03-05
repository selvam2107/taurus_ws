#!/usr/bin/env python
import cv2 as cv
from cv2 import aruco
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

class ArucoDetector:
    def __init__(self, calib_data_path, marker_size, camera_topic, cmd_vel_topic):
        self.calib_data = np.load(calib_data_path)
        self.cam_mat = self.calib_data["camMatrix"]
        self.dist_coef = self.calib_data["distCoef"] 
        self.MARKER_SIZE = marker_size

        self.marker_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.param_markers = aruco.DetectorParameters_create()

        # self.marker_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        # self.param_markers = aruco.DetectorParameters()

        self.bridge = CvBridge()
        self.twist = Twist()
        
        self.cmd_vel_pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=1)
        
        rospy.Subscriber(camera_topic, Image, self.callback_fun)

    def callback_fun(self, msg):
        try:
            # Convert ROS image message to OpenCV image
            cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            h, w = cv_img.shape[:2]
            mid_x = w / 2

            # Process the image
            gray_frame = cv.cvtColor(cv_img, cv.COLOR_BGR2GRAY)
            marker_corners, marker_IDs, _ = aruco.detectMarkers(gray_frame, self.marker_dict, parameters=self.param_markers)

            if marker_corners:
                rVec, tVec = aruco.estimatePoseSingleMarkers(marker_corners, self.MARKER_SIZE, self.cam_mat, self.dist_coef)
                total_markers = range(0, marker_IDs.size)
                for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
                    cv.polylines(cv_img, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA)
                    corners = corners.reshape(4, 2).astype(int)
                    
                    # Calculate the distance
                    distance = np.sqrt(tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2)
                    
                    # Draw the pose of the marker
                    aruco.drawAxis(cv_img, self.cam_mat, self.dist_coef, rVec[i], tVec[i], 4)
                    
                    mid_point1 = int((corners[0][0] + corners[2][0]) / 2)
                    mid_point2 = int((corners[0][1] + corners[2][1]) / 2)

                    cv.circle(cv_img, (320, 240), 5, (0, 0, 0), -1)
                    cv.circle(cv_img, (mid_point1, mid_point2), 5, (0, 0, 0), -1)

                    self.twist.linear.x = 0.1
                    self.twist.angular.z = 0.0
                    self.cmd_vel_pub.publish(self.twist)

                    if distance <= 50:
                        self.twist.linear.x = 0
                        self.twist.angular.z = 0
                        print("stop")
                    if mid_point1 <= mid_x <= mid_point1:
                        self.twist.linear.x = 0.02
                        self.twist.angular.z = 0
                        print("going straight")
                    elif mid_x > mid_point1:
                        self.twist.angular.z = 0.02
                        print("turning left")

                    elif mid_x < mid_point1:
                        self.twist.angular.z = -0.02
                        print("turning right")
                    
                    self.cmd_vel_pub.publish(self.twist)
            else:
                self.twist.linear.x = 0
                self.twist.angular.z = 0
                self.cmd_vel_pub.publish(self.twist)

            cv.imshow("frame", cv_img)
            cv.waitKey(1)
        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {0}".format(e))

if __name__ == "__main__":
    rospy.init_node("aruco_detect", anonymous=True)

    calib_data_path = "/home/ssapl/testbot_ws/src/hw_t/calib_data/MultiMatrix.npz"
    marker_size = 9.5  # centimeters
    camera_topic = "/camera/color/image_raw"
    cmd_vel_topic = "/robot/cmd_vel"

    aruco_detector = ArucoDetector(calib_data_path, marker_size, camera_topic, cmd_vel_topic)

    rospy.spin()

    cv.destroyAllWindows()
