
#!/usr/bin/env   python3.6

from pymodbus.client.sync import ModbusSerialClient as client
from pymodbus.payload import BinaryPayloadDecoder as dec
from pymodbus.constants import Endian
from std_msgs.msg import Int32
from std_msgs.msg import String
import time
import redis
import rospy
red= redis.Redis(host= 'localhost',port= '6379')
def two_cmp(val, bits):
    if val > 2**(bits-1):
            #val = val - 4294967296
            val= val-2**bits
    return val

def getBits(val, bits):
    bit_list=[]
    if val>0:
        for i in range(0, bits):
            if val & 2**i == 2**i:
                bit_list.append(i)
                
    return bit_list

def end():
    stopJog()
    print("close connection")
    mod.close()


#--------------------------------------


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
        

def longRead(add, slave, mode, prev):
    global motor_status
    try:
        result= mod.read_holding_registers(address= add, count=2, unit= slave)
        decoder= dec.fromRegisters(result.registers, Endian.Big)
        motor_status=1
        if mode:
            decoder.decode_32bit_uint
        return(decoder.decode_32bit_int())

    except AttributeError as e:
        print("wkebdbib")
        print("error1: ", e, end= " \t")
        print("prev= ", prev)
        motor_status=0
        return prev

    '''
    value= mod.read_holding_registers(address= add, count=2, unit= slave)
    en0 = abs(value.getRegister(1))
    en1= abs(value.getRegister(0)*(2**16))
    en_value= (en0+ en1)
    if mode==1:
        return(two_cmp(en_value, 32))
    '''
    
    

def writeRegister(add, val, slave):
    global motor_status
    rd= mod.write_register(address= add, value= val, unit=slave)
    motor_status=1

def longWrite(add, value, slave):
    global motor_status
    val= (value+ (1<<32))%(1<<32)
    msb= (val>>16)
    lsb= (val& 65535)
    r1= mod.write_registers(address= add, values= [msb, lsb], unit= slave)
    motor_status=1
#--------------------------------------------------------------------

def startJog():
    global motor_status
    writeRegister(124, 159, 1)
    writeRegister(124, 159, 2)

    if brakeStatus(1) or brakeStatus(2):
        motor_status=3
        print("brake engaged, reset alarm")
    else:
        writeRegister(124, 150, 1)
        writeRegister(124, 150, 2)
        print("Jog started")

def stopJog():
    writeRegister(124, 226, 1)
    writeRegister(124, 226, 2)
    writeRegister(124, 158, 1)
    writeRegister(124, 158, 2)
    print("Jog Stopped")

def disableMotor():
    writeRegister(124, 158, 1)
    writeRegister(124, 158, 2)
    print("Jog Stopped")

def checkTemp():
    result= mod.read_holding_registers(address= 18, count=3, unit= 1)
    print(result.registers)
    result= mod.read_holding_registers(address= 18, count=3, unit= 2)
    print(result.registers)


def readAlarm(slave):
    #val1= readRegister(0, slave,0)
    #val2= readRegister(1, slave,0)
    pub = rospy.Publisher("motor_connection", String, queue_size=10)
    pub1 = rospy.Publisher("motor_health", String, queue_size=10)
    # pub1= rospy.Publisher("motor_status", String, queue_size=10)
    
    try:
        val= longRead(0, slave,0,0)
        alarms= {0:"position error overrun", 1:"reverse prohibition limit", 2:"positive prohibition limit", 3:"over temperature", 4:"internal error", 5:"supply voltage out of range", 6:"reserved", 7:"drive overcurrent", 8:"reserved", 9:"motor encodeer not connected",
                10:"communication exception", 11:"reserved", 12:"vent failure", 13:"motor overload protection", 14:"reserved", 15:"unsuaal start alarm", 16:"input phase loss", 17:"STO", 18:"reserved", 19:"motor speed exceeds limit",
                20:"drive undervoltage", 21:"emergency stop", 22:"second encoder not connected", 23:"full closed loop deviation overrun", 24:"absolute encoder battery undervoltage", 25:"accurate position lost", 26:"absolute position overflow", 27:"communication interrupt", 28:"abosute encoder multi tuen error", 29:"abnormal motor action protection",
                30:"EtherCat communication error", 31:"Back to origin parameter configuration error"}
        '''
        if val2>0:
            for i in range(0, 16):
                if val2 & 2**i == 2**i:
                    error.append(i)
        if val1>0:
            for i in range(0, 16):
                print(i, 2**i, val1&2**i)
                if val1 & 2**i == 2**i:
                    error.append(i+16)
        '''
        error= getBits(val,32)
        #if len(error)>0: print("motor", slave, end=":  ")
        if red.get("wifi")==b"false":
            resetAlarm()
            startJog()
            setSpeed(11,0,0)
            input("press any key to continue---")
        if len(error)==0:
            pub.publish("--------motor connected----")
            pub1.publish("motor is healthy")
        for i in error:

            if i==20:
                a=getEncoder()
                red.set('')
                pub1.publish("please release emergrncy button and start navigation")
                print("----emregency pessed-----")
                input("----release and press any key to continue ---")
                resetAlarm()
                startJog()
                setSpeed(11,0,0)
            if i==10:
                print(i)
                pub1.publish("communication not happening check usb cable from motor")
            if i==9:
                print(i)
                pub1.publish("check encodcer cable")
            else:
                print(alarms[i],end=",")
        if len(error)>0 : print()
        return error
        
            
    except:
        if red.get("wifi")==b"false":
            input("press any key to continue---")
        print("----emregency pessed-----")
        pub1.publish("release emergency button and start navigation")
        input("press any key to continue---")
        resetAlarm()
        startJog()
        setSpeed(11,0,0)
        resetAlarm()
def getAlarmCode():
    return longRead(0,1,1,0), longRead(0,2,1,0)

def resetAlarm():
    writeRegister(124, 186, 1)
    writeRegister(124, 186, 2)

def brakeStatus(slave):
    val= readRegister(4, slave,0)
    #print(slave, val)
    if val & 4 == 4:
        return True
    return False

def setSpeed(motor_add,speed1,speed2):
    if (motor_add&10):
        longWrite(add=342, value=speed2, slave=2)
    if (motor_add &1):
        # print("turning2")
        longWrite(add=342, value=speed1, slave=1)
    

def getSpeed():
    vel1= readRegister(16, 1, 1)
    vel2= readRegister(16, 2, 1)
    rp=(vel1*60)/240
    rp2=(vel2*60)/240
    # print(rp,rp2,"speed")
    return vel1,vel2

def getEncoder(prev1, prev2):
    enc1= longRead(10, 1, 0,prev1)
    enc2= longRead(10, 2, 0,prev2)
    # enc1=-(enc1)
    # enc2=-(enc2)
    # print(enc1,enc2)
    return enc1, enc2

def setEncoder(enc):
    print("SetEncoder: ",enc)
    # print(getEncoder(slave,prev))
    longWrite(125, enc[0], 1)
    writeRegister(124, 0x98, 1)
    longWrite(125, enc[1], 2)
    writeRegister(124, 0x98, 2)
    # print("getEncoder(): ", getEncoder(1, -2000),",",getEncoder(1, -2000))

def getCurrent():
    print("current - ")
    print(readRegister(30, 1, 1), readRegister(30, 2,1))
    return readRegister(30, 1, 1), readRegister(30, 2,1)

def getStatus(slave):
    val= longRead(2, slave,0,0)
    lst= getBits(val,32)
    return lst

mod = client(method='rtu', timeout=0.03, parity='N', baudrate=19200,port='/dev/ttyUSB0')
print("Motor connection status: ",mod.connect())
time.sleep(0.2)
# rospy.init_node('motor_status')




left=2
right=1
motor_status=0
resetAlarm()