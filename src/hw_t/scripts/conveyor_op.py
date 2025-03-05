#!/usr/bin/env python3
from pymodbus.payload import BinaryPayloadDecoder as dec
from pymodbus.constants import Endian
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
    
def longWrite(value):
    global motor_status
    val= (value+ (1<<32))%(1<<32)
    msb= (val>>16)
    lsb= (val& 65535)
    r1= mod.write_register(address= 30, value= msb, unit= slave)
    r2= mod.write_register(address= 31, value= lsb, unit= slave)

def setOpcode(code,slave):
    writeRegister(124,code,slave)


def startJog():
    
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
	
	rd= mod.write_register(address= 48, value= 750, unit=slave)

def write1():

	vel1=65536-750
	rd= mod.write_register(address= 48, value= vel1, unit=slave)
 
# def feedPosition(value,speed):
 
#     position= int(value*10000)
#     enableMotor()
#     longWrite(position)
#     writeRegister(29,speed,slave)
#     setOpcode(0x67,slave)
#     pass

def move_up():
    global slave
    value=-1000
    speed=12000
    
    position= int(value*10000)
    enableMotor()
    longWrite(position)
    writeRegister(29,speed,slave)
    setOpcode(0x67,slave)
  


def move_down():
    value=0
    speed=12000
    
    position= int(value*10000)
    enableMotor()
    longWrite(position)
    writeRegister(29,speed,slave)
    setOpcode(0x67,slave)
    


#----------------conveyor------------
# while True:
#     i=int(input("enter:"))
#     if i==1:
#         write()
#         startJog()

#     elif i==2:
#         write1()
#         startJog()

#     elif i==3:
#         stopJog()
#     elif i==4:
#         print("ehgr")
        
#     elif i==5:

