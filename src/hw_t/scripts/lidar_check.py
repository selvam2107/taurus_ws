#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image as msg_Image
from cv_bridge import CvBridge, CvBridgeError
import sys
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import os
from geometry_msgs.msg import Twist
import redis
red= redis.Redis(host= 'localhost',port= '6379')
class ImageListener:
    def __init__(self, topic,timeout=5):
        self.topic = topic
        self.bridge = CvBridge() 
        s=rospy.get_published_topics()
        self.pub=rospy.Publisher("lidar_status",String,queue_size=10)
        # print("dihjb")
        try:
            rospy.wait_for_message(self.topic, LaserScan, timeout=timeout)
            # rospy.loginfo("Topic '{self.topic}' is actively publishing.")
            re="lidar is OK "
            self.pub.publish(re)
            self.sub = rospy.Subscriber(topic, LaserScan, self.imageDepthCallback)
        except rospy.ROSException:
            # raise Exception("Topic  is not actively publishing messages within {timeout} seconds.")
            print("djh")
            re="lidar is not working propery please check lidar cable and ip address"
            self.pub.publish(re)
            listener = ImageListener(self.topic)

        

    def imageDepthCallback(self, data):
        print("sij")
        try:
            re="lidar is ok"
            self.pub.publish(re)
         
            # if (cv_image[pix[1], pix[0]])<=180:
            #     twist.linear.x = 0
            # else:
            #     twist.linear.x = 0.02
            # cmd_vel_pub.publish(twist)
        except CvBridgeError as e:
            print(e)
            return


if __name__ == '__main__':
    rospy.init_node("depth_image_processor")
    topic = '/scan'  # check the depth image topic in your Gazebo environmemt and replace this with your
    listener = ImageListener(topic)
    rospy.spin()

