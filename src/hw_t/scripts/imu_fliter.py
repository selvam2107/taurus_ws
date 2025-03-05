#! /usr/bin/env python3
import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import Int32
def callback(msg):
    global vel1,vel2,pub,count

    while (-6<=vel1<=6) and (-6<=vel2<=6):

        rospy.Subscriber('wheel1/speed',Int32,callback1)
        rospy.Subscriber('wheel2/speed',Int32,callback2)
        # imu=msg
        
        
        # print(imu)
        pub.publish(msg)
    else:
        print(vel1,vel2)
        print("dsojno")
        pub.publish(msg)
def callback1(msg):
    global vel1
    vel1=msg.data
def callback2(msg):
    global vel2
    vel2=msg.data


if __name__== "__main__":
    vel1=0
    vel2=0
    count=0
    rospy.init_node("imu_filter")
    rospy.Subscriber("imu/data",Imu,callback)
    pub=rospy.Publisher('imu/data1',Imu)
    rospy.spin()