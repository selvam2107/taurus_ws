#!/usr/bin/env python3

import rospy
import time
from std_msgs.msg import Int32, Float32
from geometry_msgs.msg import Twist
from math import pi
import pymongo
import datetime
import redis

# Redis setup
red = redis.Redis(host='localhost', port=6379)

# Global variables
cumulative_data = {
    "wheel1_distance": 0,
    "wheel2_distance": 0,
    "total_distance": 0,
    "termination_count": 0,
    "total_time": 0,
}
last_save_time = None
shutdown_called = False

# MongoDB client


# Wheel and robot parameters
dia = 0.3  # Wheel diameter
gear_ratio = 60  # Gear ratio
odo1, odo2 = 0, 0  # Odometry counters
f1, f2 = True, True  # Flags for initial encoder values
ini1, ini2 = 0, 0  # Initial encoder values

# ROS Publisher
distance_pub = None  # Publisher for total distance

def store_data():
    """
    Function to store data every 15 minutes or on shutdown.
    """
    global b_current, cumulative_data, last_save_time,d3, col, odo1, odo2, shutdown_called,time_interval,d2,terminated
    dia=0.25
    gear_ratio=40
    now = datetime.datetime.utcnow()
    elapsed_time = (now - last_save_time).total_seconds() / 60 if last_save_time else 0
    # total_distace=0
   
    wheel1=(odo1*dia*pi)/(gear_ratio*10000)
    wheel2=(odo2*dia*pi)/(gear_ratio*10000)
    total_distace=(wheel1+wheel2)/2
    print(total_distace)
    if elapsed_time >= 15 or shutdown_called:
        # Calculate distances
        for i in col.find({},{"wheel1 distance in m":1, "wheel2 distance in m":1,"termination count":1,"total_time":1,"docking_count":1,"total_distance in m":1,"battery consuption per 15 min":1,"time_interval":1}):
            s=i
            print(i)
        to=s.get("termination count",0)
        if to==1:
            d2=s.get("total_distance in m",{})
            d3=s.get("battery consuption per 15 min",{})
            time_interval=s.get("time_interval",0)
            terminated=0
            col.update_one({"_id":m},{"$set": { "termination count": terminated,}})
        wheel1=(odo1*dia*pi)/(gear_ratio*10000)
        wheel2=(odo2*dia*pi)/(gear_ratio*10000)
        total_distance=(wheel1+wheel2)/2
        time_interval=float(time_interval)
        time_interval+=15
        time_interval=str(time_interval)
        d3[time_interval]=b_current
        print(type(time_interval))
        d2[time_interval]=total_distance
        dock=red.get('dock')
        dock=int(dock)
        col.update_one({"_id":m},{"$set": { "wheel1 distance in m": wheel1,"wheel2 distance in m":wheel2,"total_distance in m":d2,"battery consuption per 15 min":d3,"time_interval":time_interval,'docking_count':dock}})
        # Publish total distance
        distance_pub.publish(total_distance)
      

        # Reset odometry counters
        odo1 = 0
        odo2 = 0
        last_save_time = now

def shutdown():
    """
    Handles program shutdown by storing the latest data.
    """
    global shutdown_called,terminated
    shutdown_called = True
    terminated+=1
    # store_data()
    col.update_one({"_id":m},{"$set": { "termination count": terminated,}})
   

    print("Program terminated, data saved.")

def encoder1_cb(msg):
  global f1,ini1
  global old_wheel1
  global odo1
  if f1:
    f1=False
    ini1=abs(msg.data)
  data=abs(abs(msg.data)-ini1)
  # print(data)
    
  diff=abs(data-old_wheel1)
  if diff>50:
    odo1+=diff
    # print("odo1: ",odo1)
  old_wheel1=data


def encoder2_cb(msg):
  global f2,ini2
  global old_wheel2
  global odo2
  if f2:
    f2=False
    ini2=abs(msg.data)
  data=abs(abs(msg.data)-ini2)
    
  diff=abs(data-old_wheel2)
  if diff>50:
    odo2+=diff
    # print("odo2: ",odo2)
  old_wheel2=abs(abs(msg.data)-ini2)
def battery(msg):
    global b_current
    b_current=msg
if __name__ == '__main__':
    rospy.init_node("data_logger")

    # Initialize publisher
    myclient = pymongo.MongoClient("mongodb://192.168.5.2:27017")
    db=myclient["taurusData1"]
    print("created")
    col=db["datainfo2"]
    # col1=db["alarm_info1"]
    #doc={"_id":1}
    #col.insert_one(doc)
    load= 0
    d2={}
    d3={}
    b_current=0
    time_interval=0
    t=datetime.datetime.now()
    d=t.strftime('%d/%m/%Y')
    print(d)
    # d='10/12/2023'
    terminated=0
    tt=datetime.datetime.utcnow()

    command_x=0
    command_z=0
    speed1=0
    speed2=0
    current1=0
    current2=0
    alarm1=None
    alarm2=None
    doc_count=0
    old_wheel1=0
    old_wheel2=0
    odo1=0
    odo2=0
    f1=True
    f2=True
    ipx=0
    ipy=0
    m=0
    old_x=command_x
    old_z=command_z
    distance_pub = rospy.Publisher('/total_distance', Float32, queue_size=10)

    rospy.on_shutdown(shutdown)

    # Subscribers
    rospy.Subscriber('wheel1/current', Int32, lambda msg: None, queue_size=1)
    rospy.Subscriber('wheel2/current', Int32, lambda msg: None, queue_size=1)
    rospy.Subscriber('robot/cmd_vel', Twist, lambda msg: None, queue_size=1)
    rospy.Subscriber('wheel1/encoder', Int32, encoder1_cb, queue_size=1)
    rospy.Subscriber('wheel2/encoder', Int32, encoder2_cb, queue_size=1)
    # rospy.Subscriber("/pack_current",Float32,battery)
    # Initialize variables
    last_save_time = datetime.datetime.utcnow()
    rate = rospy.Rate(1)  # Check every second

    # Main loop
    while not rospy.is_shutdown():
        try:   
        
            for i in col.find({},{"date":1}):
                com=i
            if com["date"]==d:
                m=i["_id"]
                #print("iwueghdiuw")
                col.update_one({"_id":i["_id"]},{"$set": { "date": d,"time":tt,"load in kg":load}})
                
            else:
                for i in col.find({},{"date":1}):
                    com=i
                m=i.get("_id",0)+1
                print(m)
                col.insert_one({"_id":m})
                col.update_one({"_id":m},{"$set": { "date": d,"time":tt,"load in kg":load,}})
        except: 
            col.insert_one({"_id":1})
            col.update_one({"_id":1},{"$set": { "date": d,"time":tt,"load in kg":load, "command_x (m/s)":None, "command_z (rad/s)":89, "wheel1_speed (RPS)":None, "wheel2_speed (RPS)": None, "wheel1_current (%)": None, "wheel2_current (%)": None, "wheel1 alarm_code":None, "wheel2 alarm_code":None}})
        # if red.get('av')==b'update':
        store_data()
        rate.sleep()
