#!/usr/bin/env python

from simulation.srv import Addtwoints,AddtwointsResponse
import rospy

import time
import move2 as li
import move as li1

# import lift_functions as li

def conveyor_op(req):
    s=req.strt
    print(s)
    data=AddtwointsResponse()
    if  s==1:
        li1.move_up()
        data.ok=s
    elif s==2:
        li.forward()
        li.startJog()
        time.sleep(2)
        li.stopJog()
        print("forward")
        data.ok=s
    elif s==3:
        li1.move_down()
        data.ok=s
    elif s==4:
        li.reverse()
        li.startJog()
        time.sleep(2)
        li.stopJog()
        print("reverse")
        data.ok=s
    return data
  
def conveyor_server():
    rospy.init_node('conveyor')
    s = rospy.Service('conveyor_op', Addtwoints, conveyor_op)
    print("Ready to add two ints.")
    rospy.spin()

if __name__ == "__main__":
    conveyor_server()