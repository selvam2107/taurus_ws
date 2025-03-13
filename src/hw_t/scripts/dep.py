#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image as msg_Image
from cv_bridge import CvBridge, CvBridgeError
import sys
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
        self.pub=rospy.Publisher("camera_status",String,queue_size=10)
        # print("dihjb")
        try:
            rospy.wait_for_message(self.topic, msg_Image, timeout=timeout)
            # rospy.loginfo("Topic '{self.topic}' is actively publishing.")
            re="camera is healthy"
            self.pub.publish(re)
            self.sub = rospy.Subscriber(topic, msg_Image, self.imageDepthCallback)
        except rospy.ROSException:
            # raise Exception("Topic  is not actively publishing messages within {timeout} seconds.")
            # print("djh")
            re="camera is not working propery please check camera cable or restart the system"
            self.pub.publish(re)
            listener = ImageListener(self.topic)

        

    def imageDepthCallback(self, data):
        print("sij")
        try:
            re="camera is healthy"
            self.pub.publish(re)
            twist=Twist()
            cmd_vel_pub = rospy.Publisher('/robot/cmd_vel',Twist, queue_size=1)
            cv_image = self.bridge.imgmsg_to_cv2(data, data.encoding)
            pix = (data.width/2, data.height/2)
            sys.stdout.write('%s: Depth at center(%d, %d): %f(mm)\r' % (self.topic, pix[0], pix[1], cv_image[pix[1], pix[0]]))
            sys.stdout.flush()
            distance=cv_image[pix[1], pix[0]]
            distance=str(distance)
            red.set('distance',distance)
            distance=red.get('distance')
            distance=int(distance)
            
            # if (cv_image[pix[1], pix[0]])<=180:
            #     twist.linear.x = 0
            # else:
            #     twist.linear.x = 0.02
            # cmd_vel_pub.publish(twist)
        except CvBridgeError as e:
            red.set('distance',0)
            print(e)
            return


if __name__ == '__main__':
    rospy.init_node("depth_image_processor")
    topic = '/camera/depth/image_rect_raw'  # check the depth image topic in your Gazebo environmemt and replace this with your
    listener = ImageListener(topic)
    rospy.spin()

