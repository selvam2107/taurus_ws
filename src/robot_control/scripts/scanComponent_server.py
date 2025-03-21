#!/usr/bin/env python3.6
import rospy
import opcua as op
from opcua import ua
import time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import redis
import actionlib
from robot_control.msg import aruco_detectAction, aruco_detectFeedback, aruco_detectResult
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
            "scan_component", aruco_detectAction, execute_cb=self.execute_cb, auto_start=False)
        self.a_server.start()
        print("feirh")
    def execute_cb(self, goal):
        self.goal = goal  # Set the goal attribute
        self.feedback = aruco_detectFeedback()
        self.result = aruco_detectResult()
        self.detecting = True  # Start detecting when a goal is received
        s=str(self.goal)
        s=int(s[-1])
        print(s)
        # input()
        print("cwhbug")
        # move2.write()
        # move2.startJog()
        
        twist = Twist()
        # self.detecting = False
        red.set('conveyor','reverse')
        count=0
        while not rospy.is_shutdown() and self.detecting:
            try:
                count+=1
                if count==1:
                    print("dojn")
                    server_url = "opc.tcp://192.168.7.60:4880"
                    client = op.Client(server_url)
                else:
                    print("deon")
                    self.detecting=False
                    if self.a_server.is_preempt_requested():
                        rospy.loginfo('Preempted ArucoDetection')
                        

                        self.a_server.set_preempted()
                        self.detecting = False
                        print(bool(s))
                        return

            except:
                print("deon")
                self.detecting=False
                if self.a_server.is_preempt_requested():
                    rospy.loginfo('Preempted ArucoDetection')
                    

                    self.a_server.set_preempted()
                    self.detecting = False
                    print(bool(s))
                    return

            try:
                client.connect()
                print("Connected to OPC UA Server")

                # root = client.get_root_node()
                # print(f"Root node: {root}")
                # print("Browsing root node's children:")
                # for child in root.get_children():
                #     print(child)

                node_id = "ns=1;i=304"  
                node = client.get_node(node_id)
                value = node.get_value()
                # value_6 = value[0:7]
                # print(f"Value of node {node_id}: {value}")

                # print(f"value of first 6 bits {node_id}: {value}")
                # print(f"length of array {len(value)}")
                # set_bit_in_array(value,9)


                index_values = [1,0]
                for toggel in index_values:
                    value[5] = toggel
                    node.set_value(value, ua.VariantType.Int16)
                    # input()
                    value1 = node.get_value()[:20]
                    print(value1)
                if s==1:
                    value[39] = 1
                    node.set_value(value, ua.VariantType.Int16)
                    time.sleep(2)
                    while True:
                        value = node.get_value()
                        value_41 = value[39]
                        print(value_41)
                        if value_41==1:
                            # print("complted")
                            pass
                        else:
                            break
                if s==2:
                    value[40] = 0
                    node.set_value(value, ua.VariantType.Int16)
                    # time.sleep(2)
                    while True:
                        value = node.get_value()
                        value_41 = value[40]
                        print(value_41)
                        if value_41==0:
                            # print("complted")
                            pass
                        else:
                            break
                            
                # new_value = 42
                # node.set_value(new_value, ua.VariantType.Int32)
                # print(f"New value of node {node_id}: {node.get_value()}")
            # finally:

                client.disconnect()
                print("Disconnected from OPC UA Server")
                self.detecting=False
                if self.a_server.is_preempt_requested():
                    rospy.loginfo('Preempted ArucoDetection')
                    

                    self.a_server.set_preempted()
                    self.detecting = False
                    print(bool(s))
                    return
            except Exception as e:
                print(e)
        if self.detecting:
            self.result.distance_reached = "pick/drop completed"
            self.a_server.set_succeeded(self.result)
        elif self.a_server.is_active():
            self.result.distance_reached = "operation complted"
            self.a_server.set_aborted(self.result)
if __name__ == '__main__':
    rospy.init_node("conveyor", anonymous=True)
    red = redis.Redis(host='localhost', port='6379')

    # calib_data_path = "/home/ssapl/testbot1_ws/src/hw_t/calib_data/MultiMatrix.npz"
    # # marker_size = 6.5  # centimeters
    # camera_topic = "/scan"
    cmd_vel_topic = "/robot/cmd_vel"

    aruco_detector = motoraction()
    
    rospy.Rate(100)
    rospy.spin()