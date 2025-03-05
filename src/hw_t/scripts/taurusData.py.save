#! /usr/bin/env python3

import rospy
import time
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from math import pi
import pymongo
import datetime
import csv
import time
import redis
red=redis.Redis(host='localhost',port=6379)
def end():
    
    global odo1, odo2,m,alarm1,alarm2,tt
    print(alarm1)
    dia=0.3
    gear_ratio=60
    global col
    global wheel1,wheel2
    s=0
    g=0
    n=0
    count=0
    alarmv1=0
    alarmv2=0
    e=datetime.datetime.utcnow()
    tot=(e - tt).total_seconds()
    tot=tot/60
    print(tot)

    # t2=int(et[0:2])
    # t3=int(et[3:])
    # print(t2,t3,"huuoouio")
    # t4=int(tt[0:2])
    # t5=int(tt[3:])
    # print(t4,t5,"start")
    # t6=t2-t4
    # t7=str((t3-t5))
    # if len(t7)>2:
    #     t7=int()
    # total_time=str(t6)+':'+str(t7)
   
    wheel1=(odo1*dia*pi)/(gear_ratio*10000)
    wheel2=(odo2*dia*pi)/(gear_ratio*10000)
    total_distace=(wheel1+wheel2)/2
    
    for i in col.find({},{"wheel1 distance in m":1, "wheel2 distance in m":1,"termination count":1,"total_time":1}):
        s=i
        print(i)
    g=s.get("wheel1 distance in m",0)+wheel1
    n=s.get("wheel2 distance in m",0)+wheel2
    tm=s.get("total_time",0)+tot
    total_distace=(g+n)/2
    print(g)
    print(n)
    count+=s.get("termination count",0)+1
    print(count)
    col.update_one({"_id":m},{"$set": { "wheel1 distance in m": g,"wheel2 distance in m":n,"total_distance in m":total_distace,"termination count":count,"total_time":tm}})
    if alarm1!=None or alarm2!=None:
       
        alarmv1=readAlarm(1,alarm1)
        alarm2v=readAlarm(2,alarm2)
        col1.insert_one({"_id":tt})
        col1.update_one({"_id":tt},{"$set":{"alarm1":alarmv1,"alarm2":alarm2v}})
def getBits(val, bits):
    bit_list=[]
    if val>0:
        for i in range(0, bits):
            if val & 2**i == 2**i:
                bit_list.append(i)
    return bit_list
def readAlarm(slave,alarm):
    #val1= readRegister(0, slave,0)
    #val2= readRegister(1, slave,0)
    try:
        val= alarm
        alarms= {0:"position error overrun", 1:"reverse prohibition limit", 2:"positive prohibition limit", 3:"over temperature", 4:"internal error", 5:"supply voltage out of range", 6:"reserved", 7:"drive overcurrent", 8:"reserved", 9:"motor encodeer not connected",
                10:"communication exception", 11:"reserved", 12:"vent failure", 13:"motor overload protection", 14:"reserved", 15:"unsuaal start alarm", 16:"input phase loss", 17:"STO", 18:"reserved", 19:"motor speed exceeds limit",
                20:"drive undervoltage", 21:"emergency stop", 22:"second encoder not connected", 23:"full closed loop deviation overrun", 24:"absolute encoder battery undervoltage", 25:"accurate position lost", 26:"absolute position overflow", 27:"communication interrupt", 28:"abosute encoder multi tuen error", 29:"abnormal motor action protection",
                30:"EtherCat communication error", 31:"Back to origin parameter configuration error"}
        
        '''if val2>0:
            for i in range(0, 16):
                if val2 & 2**i == 2**i:
                    error.append(i)
        if val1>0:
            for i in range(0, 16):
                print(i, 2**i, val1&2**i)
                if val1 & 2**i == 2**i:
                    error.append(i+16)'''
        
        error= getBits(val,32)
        print(error)
        for i in error:
            print(alarms[i])
            return alarms[i]
    except:
        pass


def current1_cb(msg):
    global current1
    current1= msg.data

def current2_cb(msg):
    global current2
    current2= msg.data
   

def speed1_cb(msg):
    global speed1
    speed1= msg.data

def speed2_cb(msg):
    global speed2
    speed2= msg.data
    
def alarm1_cb(msg):
    global alarm1
    alarm1= msg.data

def alarm2_cb(msg):
    global alarm2
    alarm2= msg.data

def cmd_vel_cb(msg):
    global command_x, command_z

    command_x=msg.linear.x
    command_z=msg.angular.z


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
    db=myclient["taurusData1"]
    print("created")
    col=db["datainfo1"]
    col1=db["alarm_info1"]
    #doc={"_id":1}
    #col.insert_one(doc)
    load= int(input("enter load"))
    t=datetime.datetime.now()
    d=t.strftime('%d/%m/%Y')
    
    tt=datetime.datetime.utcnow()
    ltime=time.localtime()
    print(tt)
    '''if jnfie:
    file_path="/home/av/full_data_"+str(load)+"kg"+str(ltime.tm_mday)+str(ltime.tm_mon)+str(ltime.tm_year)+".csv"
    file=open(file_path, "a", newline="")
    file.write("")
    writer=csv.writer(file)
    writer.writerow(["Time", "command_x (m/s)", "command_z (rad/s)", "wheel1_speed (RPS)", "wheel2_speed (RPS)", "wheel1_current (%)", "wheel2_current (%)", "wheel1 alarm_code", "wheel2 alarm_code", "Wheel1 Alarm", "Wheel2 Alarm"])
'''
    command_x=0
    command_z=0
    speed1=0
    speed2=0
    current1=0
    current2=0
    alarm1=None
    alarm2=None

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

    rospy.init_node("data_logger")
    # sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, callback)
    # sub = rospy.Subscriber('/move_base_simple/goal', PoseStamped, callback, queue_size=1)
    i1 = rospy.Subscriber('wheel1/current', Int32, current1_cb,queue_size=1)
    i2 = rospy.Subscriber('wheel2/current', Int32, current2_cb,queue_size=1)
    s1 = rospy.Subscriber('wheel1/speed', Int32, speed1_cb,queue_size=1)
    s2 = rospy.Subscriber('wheel2/speed', Int32, speed2_cb,queue_size=1)
    a1 = rospy.Subscriber('wheel1/alarm_code', Int32, alarm1_cb,queue_size=1)
    a2 = rospy.Subscriber('wheel2/alarm_code', Int32, alarm2_cb,queue_size=1)
    cmd = rospy.Subscriber('robot/cmd_vel', Twist, cmd_vel_cb, queue_size=1)
    e1 = rospy.Subscriber('wheel1/encoder', Int32, encoder1_cb,queue_size=1) 
    e2 = rospy.Subscriber('wheel2/encoder', Int32, encoder2_cb,queue_size=1)

    #-----update()--------
    rate=rospy.Rate(5)
  
    while not rospy.is_shutdown():
        try:   
        
            for i in col.find({},{"date":1}):
                com=i
            if com["date"]==d:
                m=i["_id"]
                #print("iwueghdiuw")
                col.update_one({"_id":i["_id"]},{"$set": { "date": d,"time":tt,"load in kg":load, "command_x (m/s)":command_x, "command_z (rad/s)":command_z, "wheel1_speed (RPS)":	(speed1/60.0),"wheel2_speed (RPS)":(speed2/60.0), "wheel1_current (%)": (current1/10.0), "wheel2_current (%)": (current2/10.0), "wheel1 alarm_code":alarm1, "wheel2 alarm_code":alarm2}})
                
            else:
                for i in col.find({},{"date":1}):
                    com=i
                m=i.get("_id",0)+1
                print(m)
                col.insert_one({"_id":m})
                col.update_one({"_id":m},{"$set": { "date": d,"time":tt,"load in kg":load, "command_x (m/s)":command_x, "command_z (rad/s)":command_z, "wheel1_speed (RPS)":(speed1/60.0),"wheel2_speed (RPS)":(speed2/60.0), "wheel1_current (%)": (current1/10.0), "wheel2_current (%)": (current2/10.0), "wheel1 alarm_code":alarm1, "wheel2 alarm_code":alarm2}})
        except: 
            col.insert_one({"_id":1})
            col.update_one({"_id":1},{"$set": { "date": d,"time":tt,"load in kg":load, "command_x (m/s)":None, "command_z (rad/s)":89, "wheel1_speed (RPS)":None, "wheel2_speed (RPS)": None, "wheel1_current (%)": None, "wheel2_current (%)": None, "wheel1 alarm_code":None, "wheel2 alarm_code":None}})
        # if red.get('av')==b'update':
        #     end()
        #     red.set('av','no')
        
    #rospy.on_shutdown(end)
   
    rospy.on_shutdown(end)
