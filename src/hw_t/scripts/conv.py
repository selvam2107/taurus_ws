#!/usr/bin/env python3.6
from pymodbus.client.sync import ModbusSerialClient as client
import time
mod = client(method='rtu', timeout=0.5, parity='N', baudrate=9600,port='/dev/ttyUSB1')
print(mod.connect())
slave=1

def writeRegister(add, value, slave):
    global motor_status
    rd= mod.write_register(address= add, value= value, unit=slave)


def two_cmp(val, bits):
    if val > 2**(bits-1):
            #val = val - 4294967296
            val= val-2**bits
    return val
    

def readRegister(add, slave, mode):
    global motor_status
    try:
        read= mod.read_holding_registers(address= add, count= 1, unit= slave)
        read0= read.getRegister(0)
        if mode==1:
            return(two_cmp(read0, 16))
        motor_status=1
        return(read0)
    except:
        motor_status=0
        return 0


def startJog():
    global motor_status
    enableMotor()
    writeRegister(124, 150, slave)
    print("Jog started")

def stopJog():
    writeRegister(124, 226, slave)
    disableMotor()
    print("Jog Stopped")

def disableMotor():
    writeRegister(124, 158, slave)

def enableMotor():
    writeRegister(124, 159, slave)

def resetAlarm():
    writeRegister(124, 186, slave)

def write():
	
	rd= mod.write_register(address= 48, value= 2000, unit=slave)

def write1():

	vel1=65536-2000
	rd= mod.write_register(address= 48, value= vel1, unit=slave)


# stopJog()
# write()

while True:
    i=int(input("enter:"))
    if i==1:
        write()
        startJog()

    elif i==2:
        write1()
        startJog()

    elif i==3:
        stopJog()