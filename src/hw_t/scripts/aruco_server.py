#!/usr/bin/env python
import rospy
import cv2 as cv
from cv2 import aruco
import numpy as np
import tf
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ArucoTfPublisher:
    def __init__(self, calib_data_path, marker_size, camera_topic):
        # Load calibration data
        self.calib_data = np.load(calib_data_path)
        self.cam_mat = self.calib_data["camMatrix"]
        self.dist_coef = self.calib_data["distCoef"]
        self.marker_size = marker_size

        # Initialize ArUco marker dictionary and parameters
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.aruco_params = aruco.DetectorParameters_create()

        # Initialize CvBridge for converting ROS Image messages to OpenCV images
        self.bridge = CvBridge()

        # Initialize tf broadcaster
        self.tf_broadcaster = tf.TransformBroadcaster()

        # Subscribe to the camera topic
        rospy.Subscriber(camera_topic, Image, self.image_callback)

    def image_callback(self, msg):
        try:
            # Convert ROS image message to OpenCV image
            frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            # Detect ArUco markers in the frame
            corners, ids, _ = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)

            if ids is not None:
                # If markers are detected, estimate pose
                rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.cam_mat, self.dist_coef)

                for i, marker_id in enumerate(ids):
                    # Draw marker and its axis
                    aruco.drawDetectedMarkers(frame, corners)
                    aruco.drawAxis(frame, self.cam_mat, self.dist_coef, rvecs[i], tvecs[i], 0.1)

                    # Broadcast tf for the detected marker
                    self.publish_marker_tf(marker_id[0], tvecs[i][0], rvecs[i][0])

            # Display the frame (for debugging purposes)
            # cv.imshow("Aruco Marker Detection", frame)
            # cv.waitKey(1)

        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {0}".format(e))

    def publish_marker_tf(self, marker_id, tvec, rvec):
        # Convert rotation vector to quaternion
        rotation_matrix, _ = cv.Rodrigues(rvec)
        qw = np.sqrt(1 + rotation_matrix[0, 0] + rotation_matrix[1, 1] + rotation_matrix[2, 2]) / 2
        qx = (rotation_matrix[2, 1] - rotation_matrix[1, 2]) / (4 * qw)
        qy = (rotation_matrix[0, 2] - rotation_matrix[2, 0]) / (4 * qw)
        qz = (rotation_matrix[1, 0] - rotation_matrix[0, 1]) / (4 * qw)

        # Publish the transform
        self.tf_broadcaster.sendTransform(
            (tvec[0], tvec[1], tvec[2]),  # Position
            (qx, qy, qz, qw),             # Orientation as quaternion
            rospy.Time.now(),
            "marker_" + str(marker_id), # Child frame ID (marker-specific)
            "camera_link"                 # Parent frame ID (camera frame)
        )

if __name__ == "__main__":
    rospy.init_node("aruco_tf_publisher", anonymous=True)

    # Parameters
    calib_data_path = "/root/testbot_ws/src/hw_t/calib_data/MultiMatrix.npz"  # Replace with your calibration file path
    marker_size = 0.1  # Marker size in meters (e.g., 10 cm)
    camera_topic = "/camera/color/image_raw"  # Replace with your camera topic

    # Initialize and run the ArUco Tf publisher
    aruco_tf_publisher = ArucoTfPublisher(calib_data_path, marker_size, camera_topic)
    rospy.spin()
    cv.destroyAllWindows()
