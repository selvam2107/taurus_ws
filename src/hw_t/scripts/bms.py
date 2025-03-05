#!/usr/bin/env python3
import rospy
from pymodbus.client.sync import ModbusSerialClient as client
from std_msgs.msg import Int32,Float32
mod = client(method='rtu', timeout=0.5, parity='N', baudrate=115200,port='/dev/ttyUSB2')
print(mod.connect())

def bat():
	pc=0
	pv=0
	soc_pub=0
	pub = rospy.Publisher("pack_voltage", Float32, queue_size=10)
	pub1 = rospy.Publisher("pack_current", Float32, queue_size=10)
	pub2 = rospy.Publisher("soc", Int32, queue_size=10)
	rospy.init_node("battery",anonymous=True)
	while not rospy.is_shutdown():
		try:
			read= mod.read_input_registers(address= 0, count=58, unit= 1)
			pack_voltage=read.getRegister(0)
			pack_current=read.getRegister(1)
			soc=read.getRegister(9)
			print(pack_voltage/100)
			print(soc/100)
			print(pack_current/100000)
			soc_pub = int(soc/100)
			pc = round(pack_current/100000,2)
			pv = (pack_voltage/100)
		except Exception as e:
			print("pack_current",pc)
			print("pack_voltage",pv)
			print("soc",soc_pub)
			print(e)
		pub.publish(pv)
		pub1.publish(pc)
		pub2.publish(soc_pub)
			
if __name__=='__main__':
	try:
		bat()
	except rospy.ROSInterruptException:
		pass

		

