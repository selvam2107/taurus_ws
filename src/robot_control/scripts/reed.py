import opcua as op
from opcua import ua
import time
server_url = "opc.tcp://192.168.7.60:4880"
client = op.Client(server_url)

try:
    client.connect()
    print("Connected to OPC UA Server")
    node_id = "ns=1;i=304"  
    node = client.get_node(node_id)
    while True:
       
        # node = client.get_node(node_id)
        # root = client.get_root_node()
        # print(f"Root node: {root}")
        # print("Browsing root node's children:")
        # for child in root.get_children():
        #     print(child)

        
        value = node.get_value()
        v=value[39]
        print(v)
except:
    pass