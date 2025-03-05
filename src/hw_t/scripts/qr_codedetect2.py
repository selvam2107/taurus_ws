#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from geometry_msgs.msg import Twist
import numpy 
import redis
red= redis.Redis(host= 'localhost',port= '6379')
import time
import actionlib
from hw_t.msg import distanceAction,distanceFeedback,distanceResult,distanceGoal
# from pypylon import pylon
from pyzbar.pyzbar import decode
image_sub=0
rm=0
class QRCodeDetector:
    def __init__(self):
        global image_sub
        rospy.init_node('qr_code_detector', anonymous=True)
        
        self.bridge = CvBridge()
        
        image_sub = rospy.Subscriber('/camera/color/image_raw', Image)

        # Physical size of the QR code in meters (replace with the actual size)
        self.qr_code_size = 30  # Assume the QR code size is 10 cm
        self.cmd_vel_pub = rospy.Publisher('/robot/cmd_vel',Twist, queue_size=1)
        self.twist = Twist()
        self.a_server = actionlib.SimpleActionServer(
            
            "find_distance", distanceAction, execute_cb=self.image_callback, auto_start=False)
        self.a_server.start()
        
    def image_callback(self,goal,data=image_sub):
        global rm
       
        
        if goal.qr==1:
            
            print("action")
            reached=''
            feedback=distanceFeedback()
            result=distanceResult()
            rate=rospy.Rate(1)
            print(data)
            feedback.reached="hey master iam reaching goal!!!"
            self.a_server.publish_feedback(feedback)
            def endf(data,reached=reached,feedback=feedback,result=result):
                try:
                    
                    global red,rm
                    print("trying 1st try")
                    # last_distance=''
                    
                    rate = rospy.Rate(1)
                    # print("fwejhbf") 
                    image = self.bridge.imgmsg_to_cv2(data)
                    cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
                    h,w,g=cv_image.shape
                    my=h/2
                    mx=w/2
                    x=0
                    y=0
                    w=0
                    h=0
                    
                    midpoint_x=0
                    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
                    _,thresh = cv2.threshold(gray, 95, 255, cv2.THRESH_BINARY)
                    try:
                        
                        print('before inside the decode program')
                        #start = time.time()
                        #out = read_barcodes(thresh)
                        
                        barcodes = decode(thresh)
                        # print(barcodes)
                        if barcodes:
                            
                            for barcode in barcodes:
                                x, y , w, h = barcode.rect
                                #1
                                barcode_info = barcode.data.decode('utf-8')
                                cv2.rectangle(image, (x, y),(x+w, y+h), (0, 0, 255), 2)
                                
                                # feedback.reached="hey master iam reaching goal!!!"
                                # self.a_server.publish_feedback(feedback)
                                font = cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(image, barcode_info, (x + 6, y - 6), font, 1.0, (0, 0, 255), 2)
                                print('barcode data:',barcode.data)
                                print('barcode type:',barcode.type)
                                midpoint_x=x+w
                                distance=red.get('distance')
                                distance=int(distance)
                                
                                if 175<=distance<=185:
                                        print("****************************************************************************")
                                        self.twist.linear.x = 0.02
                                        self.cmd_vel_pub.publish(self.twist)
                                        time.sleep(2)
                                        self.twist.linear.x = 0.02
                                        self.cmd_vel_pub.publish(self.twist)
                                        time.sleep(2)
                                        self.twist.linear.x = 0
                                        self.twist.angular.z = 0
                                       
                                        result.distance_reached='goal_reached'
                                        self.a_server.set_succeeded(result)
                                        self.image_sub.unregister()
                                        
                                         # Unregister the subscriber
                                        QRCodeDetector()
                                        
                                elif (midpoint_x-50)<=mx<=(midpoint_x+50):
                                        self.twist.linear.x = 0.02
                                        self.twist.angular.z = 0
                                        print("go straight")
                                elif mx>(midpoint_x+50):
                                        self.twist.angular.z = 0.02
                                        print("turn left")
                                elif mx<(midpoint_x-50):
                                        self.twist.angular.z = -0.02
                                        print("turn right")
                            self.cmd_vel_pub.publish(self.twist)

                        
                 
                        
                       
                        
                        print(midpoint_x,mx)

             
                    except Exception as e:
                        print(e)
                        
                
                except Exception as e:
                    #rospy.logerr(f"Error processing image: {str(e)}")
                    pass
                
          
            self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, endf)
            rospy.spin()
           
          
                   
            

if __name__ == '__main__':
    try:
        qr_detector = QRCodeDetector()
        rospy.spin()
        
        
    except rospy.ROSInterruptException:
        pass
