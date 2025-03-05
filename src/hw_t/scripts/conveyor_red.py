#!/usr/bin/env python3
import redis
import rospy
red=redis.Redis(host='localhost',port=6379)
red2=redis.Redis(host='192.168.5.7',port=6379)
import move2
while not rospy.is_shutdown():
    if red.get('conveyor')==b'pick':
        move2.write1()
        # print(red.get('pick'))
        # red2.set('conveyor','forward')
        move2.startJog()

        while red2.get('conveyor')!=b'hold':
            print("ehi")
            pass
        red.set('conveyor',"done")
        move2.stopJog()
    elif red.get('conveyor')==b'drop':
        # red2.set('conveyor','reverse')
        move2.startJog()
        move2.write()
        # print(red.get('pick'))
        red2.set('drop1','started')
        print("started")
        while red2.get('drop1') ==b'started':
            print("waiting")
            pass
        print('en00ded')
        red.set('conveyor',"done")
        move2.stopJog()
    0