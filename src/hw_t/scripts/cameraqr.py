#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy
import math
from geometry_msgs.msg import Twist
import redis
red= redis.Redis(host= 'localhost',port= '6379')
class QRCodeDetector:
    def __init__(self):
        rospy.init_node('qr_code_detector', anonymous=True)

        self.bridge = CvBridge()

        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.image_callback)

        # Physical size of the QR code in meters (replace with the actual size)
        self.qr_code_size = 30  # Assume the QR code size is 10 cm
        self.cmd_vel_pub = rospy.Publisher('/robot/cmd_vel',Twist, queue_size=1)
        self.twist = Twist()
    def image_callback(self, data):
        try:
            image = self.bridge.imgmsg_to_cv2(data)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            r=image.shape 
            x3=int(r[0]/2)
            y3=int(r[1]/2)
            cv2.circle(image, (y3, x3), 10, (0, 255, 255), -1)
            #cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # QR code detection
            qr_code_detector = cv2.QRCodeDetector()
            value, pts, _ = qr_code_detector.detectAndDecode(gray)
        


            if value:
                # Draw bounding box around the QR code
                pts = pts.reshape((-1, 1, 2)).astype(int)
               
                '''
                start_point = (pts[0][0][0], pts[0][0][-1])
                end_point = (pts[-1][0][0], pts[-1][0][-1])
                color = (0, 0, 255)  # Blue
                thickness = 5
                cv2.line(image, start_point, end_point, color, thickness)
                '''
                point1 = (pts[0][0][0], pts[0][0][-1])
                point2 = (pts[1][0][0], pts[1][0][-1])
                point3 = (pts[-1][0][0], pts[-1][0][-1])
                color1 = (0, 255, 0) 
                color2 = (255,0, 0)
                color3 = (0, 0, 255) # Green
                radius = 10
                cv2.circle(image, point1, radius, color1, thickness=-1)
                cv2.circle(image, point2, radius, color2, thickness=-1)
                cv2.circle(image, point3, radius, color3, thickness=-1)
                # print(point1,"whdgiuew")
                cv2.polylines(image, [pts], isClosed=True, color=(255, 0, 0), thickness=1)

                thickness = 5
                cv2.line(image, point3, point2, color1, thickness)
                x1=pts[-1][0][0]
                x2=pts[1][0][0]
                y1=pts[-1][0][-1]
                y2=pts[1][0][-1]
                midpoint_x = int((x1 + x2) / 2)
                midpoint_y = int((y1 + y2) / 2)

                img = 255 * numpy.ones((500, 500, 3), dtype=numpy.uint8)


                cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

                cv2.circle(image, (midpoint_x, midpoint_y), 10, (0, 0, 0), -1)


                line_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


               

                measured_size = cv2.contourArea(pts)
                focal_length = 1000  # Example focal length in pixels (replace with the actual focal length)
                distance = (self.qr_code_size * focal_length) / measured_size
                #rospy.loginfo(f"Detected QR Code: {value}, Distance: {distance:.2f} meters")
                distance=str(distance)[0:4]
                print(distance)
                print(y3)
                if y3<midpoint_x:
                        self.twist.angular.z = -0.2
                        print("right")
                elif y3>midpoint_x:
                        self.twist.angular.z = 0.2
                        print("left")
                elif distance!="0.16":
                        self.twist.linear.x = 0.02
                elif distance=="0.16" or midpoint_x==x3:
                        self.twist.linear.x = 0
                
                        self.twist.linear.x = 0
                    
                self.cmd_vel_pub.publish(self.twist)
                # print(self.twist)
                
               
            cv2.imshow("QR Code Detection", image)
            cv2.waitKey(3)
        
        except Exception as e:
            print(e)
            #rospy.logerr(f"Error processing image: {str(e)}")

if __name__ == '__main__':
    try:
        qr_detector = QRCodeDetector()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
