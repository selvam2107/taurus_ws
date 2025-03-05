#!/usr/bin/env python3.6

import rospy
import moonsModbus
import time
from std_msgs.msg import Int32, Float32
from std_msgs.msg import String

from hw_t.srv import moonsRead, moonsReadResponse
from hw_t.srv import moonsWrite, moonsWriteResponse

def checkAlarm():
    a1=[]
    a2=[]
    a1=moonsModbus.readAlarm(1)
    a2= moonsModbus.readAlarm(2)
    return a1,a2


# ---------------------------------------------------------
def read(req):
    if (l_inv!=1 and l_inv!=-1): return
    if (r_inv!=1 and r_inv!=-1):return
    prev1= req.prev1*l_inv
    prev2= req.prev2*r_inv
    global old_motor_status
    global encoder
    data=moonsReadResponse()
    
    
    data.enc1,data.enc2=moonsModbus.getEncoder(prev1, prev2)
    data.vel1,data.vel2=moonsModbus.getSpeed()
    cur1, cur2= moonsModbus.getCurrent()
    al1, al2= moonsModbus.getAlarmCode()


    if moonsModbus.motor_status and not old_motor_status:
        moonsModbus.setEncoder(encoder)
        old_motor_status=1
    if not moonsModbus.motor_status:
        old_motor_status=0

    encoder[0]=data.enc1
    encoder[1]=data.enc2
    
    data.enc1*=l_inv
    data.vel1*=l_inv
    data.enc2*=r_inv
    data.vel2*=r_inv
    cur1*=l_inv
    cur2*=r_inv

    # The following lines are added to publish raw encoder values and speed
    enc1.data=encoder[0]
    enc2.data=encoder[1]
    pub1.publish(enc1)
    pub2.publish(enc2)
    pubs1.publish(data.vel1)
    pubs2.publish(data.vel2)
    current1.publish(cur1)
    current2.publish(cur2)
    alarm1.publish(al1)
    alarm2.publish(al2)

    checkAlarm()
    data.result=moonsModbus.motor_status
    return data

# ----------------------------------------------------------------------------------------------------------------------

def write(req):
    if (l_inv!=1 and l_inv!=-1): return
    if (r_inv!=1 and r_inv!=-1):return
    # motor_add= req.motor
    # entity= req.entity
    # value= req.value
    # moonsModbus.test()
    # return moonsWriteResponse(result=1)
    # print("-----------write----------------")
    motor_add= req.motor
    entity= req.entity
    value1= req.value1*l_inv
    value2= req.value2*r_inv

    # print("motor_add= ", motor_add, " entity= ", entity, " value= ", value)
    if (int(entity)==2):
        try:
            moonsModbus.setSpeed(motor_add, value1,value2)
            # print("Encoder: ", encoder)
        except:
            rospy.WARN("error in setSpeed Function")
        status1, status2= moonsModbus.getStatus(1), moonsModbus.getStatus(2) 
        if 5 not in status1 or 5 not in status2:
            moonsModbus.startJog()
    elif(int(entity)==3):
        try:
            moonsModbus.resetAlarm()
            rospy.INFO("Alarm has been reset")
        except:
            rospy.WARN("Error resetting alarm")
    else:
        return moonsWriteResponse(result=2)
    checkAlarm()
    return moonsWriteResponse(result=moonsModbus.motor_status)
# ---------------------------------------------------------

def server():
    rospy.init_node('moons_server')
    s1= rospy.Service('moons_read', moonsRead, read)
    s2= rospy.Service('moons_write', moonsWrite, write)
    # rospy.Subscriber("test",String, callback=cb)
    rospy.spin()

    moonsModbus.setEncoder(2,0)

if __name__== "__main__":
    left= 2
    right=1
    # The below 2 values are either 1 or -1 only
    l_inv=-1
    r_inv=1

    moonsModbus.resetAlarm()
    moonsModbus.stopJog()
    moonsModbus.setEncoder([0,0])
    moonsModbus.resetAlarm()
    moonsModbus.checkTemp()
    # moonsModbus.getCurrent()
    encoder=[0,0]
    old_motor_status=0
    pub1 = rospy.Publisher('wheel1/encoder', Int32, queue_size=1)
    pub2 = rospy.Publisher('wheel2/encoder', Int32, queue_size=1)
    pubs1 = rospy.Publisher('wheel1/speed', Int32, queue_size=1)
    pubs2 = rospy.Publisher('wheel2/speed', Int32, queue_size=1)
    current1 = rospy.Publisher('wheel1/current', Int32, queue_size=1)
    current2 = rospy.Publisher('wheel2/current', Int32, queue_size=1)
    alarm1 = rospy.Publisher('wheel1/alarm_code', Int32, queue_size=1)
    alarm2 = rospy.Publisher('wheel2/alarm_code', Int32, queue_size=1)
    enc1=Int32()
    enc2=Int32()
    speed=Float32()
    server()

