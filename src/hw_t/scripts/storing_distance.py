#!/usr/bin/env python3
# license removed for brevity

import time
import redis
import rospy
from geometry_msgs.msg import Twist
from math import pi
import pymongo
import datetime

from std_msgs.msg import Int32

from hw_t.msg import distance


def dist():
    global odo1,odo2
    gear_ratio=60
    dia=0.3
    get_id=int(input("enter:"))
    load= int(input("enter load"))
    t=datetime.datetime.now()
    d=t.strftime('%d/%m/%Y')

    
    s=0
    m1=0
    tt=datetime.datetime.utcnow()
    ltime=time.localtime()
 
    e=datetime.datetime.utcnow()
    tot=(e - tt).total_seconds()
    tot=tot/60
   

    col.insert_one({"_id":get_id}) 

    pub = rospy.Publisher('/travelled',distance , queue_size=10)
    rospy.init_node('status_node', anonymous=True)
    
    rate=rospy.Rate(10)


    while not rospy.is_shutdown():
        
        r_wheel=(odo1*dia*pi)/(gear_ratio*10000)
        l_wheel=(odo2*dia*pi)/(gear_ratio*10000)
        total_wheel=(r_wheel+l_wheel)/2
       
        col.update_one({"_id":get_id},{"$set": {"date":d,"load":load, "wheel1_distance": r_wheel,"wheel2_distance":l_wheel,"total_distance":total_wheel}})

        for i in col.find({},{"_id":1,"total_distance":1}):
           v=i
        the_dist=v.get("total_distance",0)+total_wheel
        col1.update_one({"_id":d},{"$set":{"total_distance":the_dist}})





        # try:   
        
        #     for i in col.find({},{"date":1}):
        #         com=i
        #     if com["date"]==d:
        #         m=i["_id"]
               
        #         col.update_one({"_id":i},{"$set": {"date":d ,"load":load}})
               
                
        #     else:
        #         for i in col.find({},{"date":1}):
        #             com=i
        #         m=i.get("_id",0)+1
        #         print(m)
        #         col.insert_one({"_id":m})
        #         # col.update_one({"_id":m},{"$set": { "wheel1_distance": l_wheel,"wheel2_distance":r_wheel,"total_distance":total_wheel}})
        #         col.update_one({"_id":m},{"$set": {"date":d ,"load":load}})


        #         # col.update_one({"_id":m},{"$set": { "date": d,"time":tt,"load in kg":load, "command_x (m/s)":command_x, "command_z (rad/s)":command_z, "wheel1_speed (RPS)":(speed1/60.0),"wheel2_speed (RPS)":(speed2/60.0), "wheel1_current (%)": (current1/10.0), "wheel2_current (%)": (current2/10.0), "wheel1 alarm_code":alarm1, "wheel2 alarm_code":alarm2}})
        # except: 
        #     col.insert_one({"_id":1})
        #     # col.update_one({"_id":1},{"$set": { "wheel1_distance": l_wheel,"wheel2_distance":r_wheel,"total_distance":total_wheel}})
        #     col.update_one({"_id":1},{"$set": {"date":d ,"load":load}})


        #     # col.update_one({"_id":1},{"$set": { "date": d,"time":tt,"load in kg":load, "command_x (m/s)":None, "command_z (rad/s)":89, "wheel1_speed (RPS)":None, "wheel2_speed (RPS)": None, "wheel1_current (%)": None, "wheel2_current (%)": None, "wheel1 alarm_code":None, "wheel2 alarm_code":None}})

        # for i in col.find({},{"wheel1_distance":1, "wheel2_distance":1, "total_distance":1}):
        #         s=i
        #         print(s)
        # g=s.get("wheel1_distance",0)+r_wheel
        # n=s.get("wheel2_distance",0)+l_wheel
        # m1=s.get("_id")
        # total_distace=(g+n)/2
        # # col.update_one({"_id":m1},{"$set": { "wheel1_distance": g,"wheel2_distance":n,"total_distance":total_distace}})

          
        msg=distance()
        msg.r_wheel=r_wheel
        msg.l_wheel=l_wheel
        msg.total_distance=total_wheel

        pub.publish(msg)
        print(msg)
        rate.sleep() 

        

     
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

if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://192.168.5.6:27017")
    db=myclient["Running_status"]
    


    col=db["taurus_distance"]
    col1=db["total_distance"]
    # col.insert_one({"_id":1,"wheel1_distance":0,"wheel2_distance":9,"total_distance":8})
   
    odo1=0
    odo2=0
    f1=True
    f2=True
    old_wheel1=0
    old_wheel2=0
    m=0
    s=0
  
    e1 = rospy.Subscriber('wheel1/encoder', Int32, encoder1_cb,queue_size=1) 
    e2 = rospy.Subscriber('wheel2/encoder', Int32, encoder2_cb,queue_size=1)
    try:
        dist()
    except rospy.ROSInterruptException:
        pass