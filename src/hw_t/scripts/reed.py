#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import redis
import actionlib
from hw_t.msg import aruco_detectAction, aruco_detectFeedback, aruco_detectResult
red=redis.Redis(host='localhost',port=6379)
class ScanActionServer:
    def __init__(self,camera_topic,cmd_vel_topic):
        # self.server = actionlib.SimpleActionServer('scan_control', aruco_detectAction, self.execute_callback, False)
        # self.server.start()
        # self.cmd_vel_pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
        # self.red = redis.Redis(host='localhost', port='6379')
        self.return_back = False
        self.detecting = False
        self.goal = None
        self.cmd_vel_pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=1)
        rospy.Subscriber(camera_topic, LaserScan, self.scan_callback)
       
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
                return

            # Detection logic is handled in the callback
            rospy.sleep(0.1)

        if self.detecting:
            self.result.distance_reached = "Detection completed"
            self.a_server.set_succeeded(self.result)
        elif self.a_server.is_active():
            self.result.distance_reached = "Detection aborted"
            self.a_server.set_aborted(self.result)

    def scan_callback(self, scan_data):
        twist = Twist()
        # distance = int(red.get('distance'))
        distance=400
        # print("wdihb")
        # if not self.detecting:
        #     return 
        if 175 <= distance <= 310:
            self.detecting = False
        if red.get("stop")==b"false":
             self.detecting = False
        # print(scan_data,"wdugug")
        for i, range_distance in enumerate(scan_data.ranges):
            angle = scan_data.angle_min + i * scan_data.angle_increment
            # print(angle,range_distance)
            if 0.65 <= angle <= 1.5:
                # print("eduhvu")
                print(angle,range_distance)
            # if -2.08<=angle<=-2.0:
            #     print(angle,range_distance)
            #     if 0.05<=range_distance<=2:
            #         if 0.8<=range_distance<=1:
            #             twist.angular.z=0.02
            #             twist.linear.x=0.0
            #             print("wyhg")
            #             # input()
            #             self.cmd_vel_pub.publish(twist)
            #         elif 1<=range_distance<1.1:
            #             twist.angular.z=-0.02
            #             twist.linear.x=0.0
            #             print("qsxhoiqw")
            #             # input()
            #             self.cmd_vel_pub.publish(twist)

            #         else:
            #             twist.angular.z=0
            #             self.cmd_vel_pub.publish(twist)
            # if 2.15<=angle<=2.18:
            #     # print(angle,range_distance,"wehbd")
                
            #     if 0<=range_distance<=6:
            #         print(range_distance)
            #         if 0.41<=range_distance<=0.52:
            #             print(range_distance)
            #             twist.angular.z=0.0
            #             twist.linear.x=0.02
            #             self.cmd_vel_pub.publish(twist)
            #             print("fkfnwqiuefbq")
            #         elif 0.4<=range_distance<=0.:
            #             print(range_distance)
            #             twist.angular.z=0.0
            #             twist.linear.x=0.02
            #             self.cmd_vel_pub.publish(twist)
            #             print("deokfnhiug3")

            #         elif range_distance<0.35:
            #             twist.angular.z=-0.02
            #             self.cmd_vel_pub.publish(twist)
            #         else:
            #             twist.angular.z=-0.02
            #             self.cmd_vel_pub.publish(twist)

            #     else:
            #             twist.linear.x=0.02
            #             twist.angular.z=0.0
            #             self.cmd_vel_pub.publish(twist)
if __name__ == '__main__':
    rospy.init_node("aruco_detect", anonymous=True)
    red = redis.Redis(host='localhost', port='6379')

    # calib_data_path = "/home/ssapl/testbot1_ws/src/hw_t/calib_data/MultiMatrix.npz"
    # marker_size = 6.5  # centimeters
    
    camera_topic = "/scan"
    cmd_vel_topic = "/robot/cmd_vel"

    aruco_detector = ScanActionServer( camera_topic, cmd_vel_topic)
    
    rospy.Rate(100)
    rospy.spin()
  