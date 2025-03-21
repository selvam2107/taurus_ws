#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import redis
import actionlib
from hw_t.msg import aruco_detectAction, aruco_detectFeedback, aruco_detectResult
red=redis.Redis(host='localhost',port=6379)
import time
# import move2
class motoraction:
    def __init__(self):
        self.return_back = False
        self.detecting = False
        self.goal = None
        self.cmd_vel_pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=1)
        self.a_server = actionlib.SimpleActionServer(
            "back", aruco_detectAction, execute_cb=self.execute_cb, auto_start=False)
        self.a_server.start()
        print("feirh")
    def execute_cb(self, goal):
        global no_obstacle
        self.goal = goal  # Set the goal attribute
        self.feedback = aruco_detectFeedback()
        self.result = aruco_detectResult()
        self.detecting = True  # Start detecting when a goal is received
        # self.c
        print("cwhbug")
        # move2.write()
        # move2.startJog()
        
        twist = Twist()
        # self.detecting = False
        red.set('conveyor','reverse')
        while not rospy.is_shutdown() and self.detecting:
            print("dwhb")

            distance=red.get("distance")
            distance=int(distance)
            while distance<3000:
                r=rospy.get_param("/distance_goal_qr", self.goal)
                if r==0:
                    self.a_server.set_preempted()
                    self.detecting = False
                    print("soho")
                    return
                rospy.Subscriber("/scan_2", LaserScan, self.callback)
                time.sleep(0.25)
                print(no_obstacle)
                if no_obstacle=='yes':
                    twist.linear.x=0
                    self.cmd_vel_pub.publish(twist)
                    print("ty")
                    
                else:
                    twist.linear.x=-0.1
                    self.cmd_vel_pub.publish(twist)
                    distance=red.get("distance")
                    distance=int(distance)
            try:
                si=red.get('dock')
                si=int(si)
                si=si+1
            except:
                si=red.set('dock','1')
                si=red.get('dock')
                si=int(si)
                si=si+1


            red.set('dock',str(si))
            self.detecting=False


            if self.a_server.is_preempt_requested():
                rospy.loginfo('Preempted ArucoDetection')
                

                self.a_server.set_preempted()
                self.detecting = False
                print(bool(s))
                return

            # Detection logic is handled in the callback
            rospy.sleep(0.1)

        if self.detecting:
            self.result.distance_reached = "pick/drop completed"
            self.a_server.set_succeeded(self.result)
        elif self.a_server.is_active():
            self.result.distance_reached = "pick/drop aborted"
            self.a_server.set_aborted(self.result)
    def callback(self,scan_data):
        global no_obstacle
        # print("wbhvh")
        for i, range_distance in enumerate(scan_data.ranges):
            angle = scan_data.angle_min + i * scan_data.angle_increment
            
            if -1.00<=angle<=-0.65:
                if range_distance==0:
                        continue
                if 0.05<=range_distance<=0.6:
                    no_obstacle='yes'
                    print(angle,range_distance)
                    print("ejhb")
                    return no_obstacle
            if -1.65<=angle<=-1.45:
                if 0.05<=range_distance<=1:   
                    no_obstacle='yes'
                    return no_obstacle
            if 0.60<=angle<=0.0:
                if 0.05<=range_distance<=1:   
                    no_obstacle='yes'
                    return no_obstacle
        else:
            no_obstacle='no'
            return no_obstacle
                    


        
if __name__ == '__main__':
    rospy.init_node("conveyor", anonymous=True)
    red = redis.Redis(host='localhost', port='6379')
    no_obstacle='no'
    # calib_data_path = "/home/ssapl/testbot1_ws/src/hw_t/calib_data/MultiMatrix.npz"
    # # marker_size = 6.5  # centimeters
    # camera_topic = "/scan"
    cmd_vel_topic = "/robot/cmd_vel"

    aruco_detector = motoraction()
    
    rospy.Rate(100)
    rospy.spin()