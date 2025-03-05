# from opcua import Client
import opcua as op
from opcua import ua
import time


server_url = "opc.tcp://192.168.7.60:4880"
client = op.Client(server_url)

try:
    client.connect()
    print("Connected to OPC UA Server")

    # root = client.get_root_node()
    # print(f"Root node: {root}")
    # print("Browsing root node's children:")
    # for child in root.get_children():
    #     print(child)

    node_id = "ns=1;i=304"  
    node = client.get_node(node_id)
    value = node.get_value()
    # value_6 = value[0:7]
    # print(f"Value of node {node_id}: {value}")

    # print(f"value of first 6 bits {node_id}: {value}")
    # print(f"length of array {len(value)}")
    # set_bit_in_array(value,9)

    value_41 = value[39]
    index_values = [1,0]
    for toggel in index_values:
        value[5] = toggel
        node.set_value(value, ua.VariantType.Int16)
        # value1 = node.get_value()[:20]
        # print(value1)
    print(value_41,"ehdg")
    count=0
    # while value_41==0:
    #         value_41 = value[39]
    #         count+=1
    #         print(value_41,count)
    #         if value_41==1:
    #             break
    # finally:
    while True:
        value = node.get_value()
        value_41 = value[39]
        print(value_41)
        if value_41==0:
            print("complted")
        else:
            break

    client.disconnect()
    print("Disconnected from OPC UA Server")

except Exception as e:
    print('error',e)
    # new_value = 42
    # node.set_value(new_value, ua.VariantType.Int32)
    # print(f"New value of node {node_id}: {node.get_value()}")
