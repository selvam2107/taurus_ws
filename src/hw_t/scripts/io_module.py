from pymodbus.client.sync import ModbusTcpClient
import rospy
import json
from std_msgs.msg import String
# Connect to ADAM-6060
client = ModbusTcpClient('192.168.7.20', port=502)
client.connect()
rospy.init_node("io_output")
pub = rospy.Publisher("io_output", String, queue_size=10)
while True:
    l={}
# Read 6 digital output states (starting from address 00017)
    response = client.read_coils(17, 1, unit=1)  # 0-based indexing (00017 is at index 16)

    if response.isError():
        print("Error reading output status")
    else:
        print("Digital Output Status:")
        for i, state in enumerate(response.bits):
            print(f"Output {i}: {'ON' if state else 'OFF'}")
            l[i]=state
    print(l)
    msg_str = json.dumps(l)
    pub.publish(msg_str)
    # Close connection
    # msg_data = {"key1": s[0], "key2": s[1], "key3": s[2],'key4':s[3],'key5':s[4],'key6':s[5],'key7':s[6],'key8':s[7]}
    client.close()
# # from pymodbus.client.sync import ModbusTcpClient


# # client = ModbusTcpClient('192.168.7.10', port=502)


# # response = client.read_discrete_inputs(0, 6)

# # if response.isError():
# #     print("Error reading inputs")
# # else:
# #     print("Digital Inputs:", response.bits)

# # client.close()
# import rospy
# from std_msgs.msg import String
# import json
# rospy.init_node("iomodule")
# def callback(msg):
#     data = json.loads(msg.data)
#     print(data)
    


# while True:
#     rospy.Subscriber("dict_topic", String, callback)
    
