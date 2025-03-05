#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import redis
import actionlib
import actionlib
from hw_t.msg import aruco_detectAction,aruco_detectGoal
from hw_t.msg import aruco_detectAction, aruco_detectFeedback, aruco_detectResult
red=redis.Redis(host='localhost',port=6379)
import time
class ScanActionServer:
    def __init__(self,camera_topic,cmd_vel_topic):
        # self.server = actionlib.SimpleActionServer('scan_control', aruco_detectAction, self.execute_callback, False)
        # self.server.start()
        # self.cmd_vel_pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
        # self.red = redis.Redis(host='localhost', port='6379')
        self.return_back = False
        self.detecting = False
        self.goal = None
        red.set("a","go")
        self.cmd_vel_pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=1)
        rospy.Subscriber(camera_topic, LaserScan, self.scan_callback)
        self.a_server = actionlib.SimpleActionServer(
            "Table_dock1", aruco_detectAction, execute_cb=self.execute_cb, auto_start=False)
        self.a_server.start()
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
        if not self.detecting:
            return 
        if 175 <= distance <= 310:
            self.detecting = False
        if red.get("stop")==b"false":
                def feedback_cb(msg):
                    print("feedback:",msg)
                # client2 = actionlib.SimpleActionClient('conveyor_drop', aruco_detectAction)
                # client2.wait_for_server()
                # goal = aruco_detectGoal()
                # result = 0
                # goal = aruco_detectGoal()
                # goal.detect = 1
                # client2.send_goal(goal, feedback_cb=feedback_cb)
                # client2.wait_for_result()
                # result = client2.get_result()
                # print("the result is", result.distance_reached)
                self.detecting = False
             
        for i, range_distance in enumerate(scan_data.ranges):
            angle = scan_data.angle_min + i * scan_data.angle_increment
            distance=red.get('distance')
            distance=int(distance)
            if 0.6<=angle<=0.62 and range_distance>1.5 and red.get('a')!=b'go'  and distance<500:
                print(range_distance,angle)
                distance=red.get('distance')
                red.set('a','go')
                distance=int(distance)
                time.sleep(5)
                sa=distance
                client2 = actionlib.SimpleActionClient('conveyor_drop', aruco_detectAction)
                client2.wait_for_server()
                goal = aruco_detectGoal()
                result = 0
                goal = aruco_detectGoal()
                goal.detect = 1
                client2.send_goal(goal, feedback_cb=feedback_cb)
                client2.wait_for_result()
                result = client2.get_result()
                print("the result is", result.distance_reached)
                while distance<=1800:
                    distance=red.get('distance')
                        
                    distance=int(distance)
                    print(distance,sa)
                    twist.linear.x=-0.1
                    self.cmd_vel_pub.publish(twist)
                s1=red.get("dock")
                # count=int(s1)
                # count+=1
                # red.set("dock",str(count))
                self.detecting = False
                return 'success'
            
                
            if -1.30<=angle<=-0.65 and red.get('a')==b'go' :
            
                    if range_distance==0:
                        continue
                    if 0.05<=range_distance<=0.8:
                        twist.angular.z=-0.02
                        twist.linear.x=0
                        self.cmd_vel_pub.publish(twist)
                        print("rotatinge2")
                        print(f"Angle: {angle:.2f} radians, Distance: {range_distance:.2f} meters1")
                        return
            if 0.45 <= angle <= 2.14:
                
                self.feedback.reached = "reaching"
                self.a_server.publish_feedback(self.feedback)
                if range_distance == 0.0:
                    continue
                elif 0.05 <= range_distance <= 0.08:
                    red.set("a","w")
                    twist.angular.z = 0
                    twist.linear.x = 0.07
                    print(f"Angle: {angle:.2f} radians, Distance: {range_distance:.2f} meters2")
                    self.cmd_vel_pub.publish(twist)
                    return
                elif 0.08 < range_distance <= 0.7:
                    if range_distance>0.08:
                    #   red.set("a","w")
                      twist.angular.z = 0.01
                    #   twist.linear.x=0.0
                      print(f"Angle: {angle:.2f} radians, Distance: {range_distance:.2f} check")
                      print("wigfiuw2iu")
                      self.cmd_vel_pub.publish(twist)
                    elif range_distance<0.07:
                       
                        twist.angular.z=-0.02
                        # twist.linear.x=0
                        self.cmd_vel_pub.publish(twist)
                        print("rotatinge")
                        print(f"Angle: {angle:.2f} radians, Distance: {range_distance:.2f} meters")
                    

                    
                else:
                    twist.angular.z = 0
                    twist.linear.x = 0.04
                    self.cmd_vel_pub.publish(twist)
           
                 
                    # else:
                    #     twist.angular.z=0
                    #     self.cmd_vel_pub.publish(twist)           
            if -0.58<=angle<=0:
            #   print(angle)
              
              if range_distance==0.0:
                  continue
              elif 0.02<=range_distance <=0.08:
                  twist.angular.z=-0.02
                  twist.linear.x=0
                #   red.set("a","w")
                  print(angle)
                  print("rotating")
                
                  # angle = scan_data.angle_min + i * scan_data.angle_increment
                  print(f"Angle: {angle:.2f} radians, Distance: {distance:.2f} meters")
                  self.cmd_vel_pub.publish(twist)
                  return
              else:
                  twist.angular.z=0
                  twist.linear.x=0.02
                #   red.set("a","w")
              
                  self.cmd_vel_pub.publish(twist)
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
  