#!/usr/bin/env python3.6

import rospy
from geometry_msgs.msg import Twist
import sys, select, os
import redis

if os.name == 'nt':
  import msvcrt
else:
  import tty, termios


red= redis.Redis(host= 'localhost',port= '6379')

MAX_LIN_VEL = 0.75
MAX_ANG_VEL = 2.0

LIN_VEL_STEP_SIZE = 0.05
ANG_VEL_STEP_SIZE = 0.05

msg = """
Controls
---------------------------
Moving around:
        w
   a    s    d
        x

w/x : increase/decrease linear velocity 
a/d : increase/decrease angular velocity 

space key, s : force stop

CTRL-C to quit
"""

e = """
Communications Failed
"""

def getKey():
    if os.name == 'nt':
      if sys.version_info[0] >= 3:
        return msvcrt.getch().decode()
      else:
        return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(target_linear_vel, target_angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s " % (target_linear_vel,target_angular_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop )
    elif input < output:
        output = max( input, output - slop )
    else:
        output = input

    return output

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
 
    vel = constrain(vel, -MAX_LIN_VEL, MAX_LIN_VEL)

    return vel

def checkAngularLimitVelocity(vel):

    vel = constrain(vel, -MAX_ANG_VEL, MAX_ANG_VEL)

    return vel

if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('Teleop1')
    pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=10)

    status = 0
    target_linear_vel   = 0.0
    target_angular_vel  = 0.0
    control_linear_vel  = 0.0
    control_angular_vel = 0.0

    try:
        print(msg)
        while(1):
            status1=0

            key = getKey()
            if key == 'w' :
                target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel,target_angular_vel))
            elif key == 'x' :
                target_linear_vel = checkLinearLimitVelocity(target_linear_vel - LIN_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel,target_angular_vel))
            elif key == 'd' :
                target_angular_vel = checkAngularLimitVelocity(target_angular_vel - ANG_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel,target_angular_vel))
            elif key == 'a' :
                target_angular_vel = checkAngularLimitVelocity(target_angular_vel + ANG_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel,target_angular_vel))
            elif key == 'r' :
                target_angular_vel = 0
                control_angular_vel= 0
                status = status + 1
                print(vels(target_linear_vel,target_angular_vel))
            elif key == ' ' or key == 's' :
                target_linear_vel   = 0.0

                control_linear_vel  = 0.0
                target_angular_vel  = 0.0
                control_angular_vel = 0.0
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'i' :
                print("Fault Reset")
                red.set("reset", "1")
            elif key == 'j' :
                print("drive started")
                red.set("drive", "start")
            elif key == 'k' :
                print("drive stopped")
                red.set("drive", "stop")
            elif key == ',' :
                print("lift DOWN")
                red.set("lift", "down")
            elif key == '.' :
                print("lift UP")
                red.set("lift", "up")
            elif key == '/' :
                print("lift EMG")
                red.set("list", "stop")
            else:
                if (key == '\x03' or key == 'q'):
                    break

            if status == 20 :
                print(msg)
                status = 0

            if control_linear_vel <=0:
                red.set("reverse", "true")
            else:
                red.set("reverse", "false")

            if red.get("drive") == b'safety':
                target_linear_vel   = 0.0

                control_linear_vel  = 0.0
                target_angular_vel  = 0.0
                control_angular_vel = 0.0
                print("Safety",vels(target_linear_vel, target_angular_vel))

            twist = Twist()

            control_linear_vel =target_linear_vel #makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/4))
            twist.linear.x = control_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0

            control_angular_vel = target_angular_vel #makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/4))
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel

            if twist.linear.x>=0.001 or twist.linear.x<=-0.001:
                red.set("light","blink")
            elif twist.angular.z>=0.005 or twist.angular.z<=-0.005:
                red.set("light","blinkr")
            else:
                red.set("light", "red")
                
 
            #twist.linear.x=target_linear_vel
            #twist.angular.z = target_angular_vel

            pub.publish(twist)
            

    except Exception as error:
        print(error)
        print(e)

    finally:
        #twist = Twist()
        #twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        #twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        #pub.publish(twist)
        red.set("light", "off")
        pass

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
