#!/usr/bin/env python3
import rospy
from pymodbus.client.sync import ModbusTcpClient

# Replace with your ADAM-6060 IP address
ADAM_IP = "192.168.7.20"
PORT = 502  # Default Modbus TCP port

client = ModbusTcpClient(ADAM_IP, port=PORT)
client.connect()

# OUTPUT_INDEX = 19  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
# client.write_coil(OUTPUT_INDEX, True)
try:    
    n=rospy.get_param('navigation')
except:
    rospy.set_param('navigation',0)
# Writing to Coil (DO0) - Address 17 (0-based: 16)
try:
    while not rospy.is_shutdown():
        n=rospy.get_param('navigation')
        if n==1:
            OUTPUT_INDEX = 19  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, False)
            OUTPUT_INDEX = 17  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, True)
            OUTPUT_INDEX = 18  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, False)  # Turn ON
        # client.write_coil(OUTPUT_INDEX, False)  # Turn OFF
        if n==3:
            OUTPUT_INDEX = 19  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, False)
            OUTPUT_INDEX = 17  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, False)
            OUTPUT_INDEX = 18  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, True)
        if n==2:
            OUTPUT_INDEX = 17  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, False)
            OUTPUT_INDEX = 19  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, True)
            
            OUTPUT_INDEX = 18  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, True)
        if n==4:
            OUTPUT_INDEX = 17  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, True)
            OUTPUT_INDEX = 19  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, True)
            
            OUTPUT_INDEX = 18  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, True)
        if n==0:
            OUTPUT_INDEX = 17
            client.write_coil(OUTPUT_INDEX, False)
            OUTPUT_INDEX = 18  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, False)

            OUTPUT_INDEX = 19  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
            client.write_coil(OUTPUT_INDEX, True)
except:
    print("uygyg")
    OUTPUT_INDEX = 19  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
    client.write_coil(OUTPUT_INDEX, False)
    OUTPUT_INDEX = 17  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
    client.write_coil(OUTPUT_INDEX, False)
    OUTPUT_INDEX = 18  # DO0 = 16, DO1 = 17, DO2 = 18, etc.
    client.write_coil(OUTPUT_INDEX, False)
    client.close()

