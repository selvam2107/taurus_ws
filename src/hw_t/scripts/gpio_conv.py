#!/usr/bin/env python3
from periphery import GPIO
import time
green_pin = GPIO(23,"out")
grey_pin = GPIO(24,"out")

try:
	while True:
		inp = int(input("enter pin: "))
		if inp==1:
			green_pin.write(True)
		elif inp==2:
			green_pin.write(True)
			grey_pin.write(True)
		else:
			green_pin.write(False)
			grey_pin.write(False)
except:
	print("--------")		
