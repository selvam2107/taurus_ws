import rospy
from rosgraph_msgs.msg import Log
from std_msgs.msg import String

# Flags to track warning state
warning_active = False  # Tracks if the lidar warning is currently active

def callback(msg):
    global warning_active,pub,pub1

    if "Could not get robot pose, cancelling reconfiguration" in msg.msg:
        if not warning_active:  # Trigger only when first detected
            print("⚠️ No scan detected!")
            warning_message = "Lidar is not working properly. Please check the lidar cable and IP address."
            pub.publish(warning_message)  # Publish only once
            # warning_active = True  # Set warning as active
            s=rospy.set_param("/lidar_camera_reset",0)
    if "No RealSense devices were found!" in msg.msg:
        print("no camera")
        s=rospy.set_param("/lidar_camera_reset",0)
        re="camera is not working propery please check camera cable or restart the system"
        pub1.publish(re)
        

    else:
        try:
            s=rospy.get_param("/lidar_camera_reset")
            if s==1:  # Only print recovery message once
                print("✅ Lidar is working fine.")
                pub.publish("lidar is healthy")  # Publish only once-
                re="camera is healthy"
                pub1.publish("camera is healthy")
                # warning_active = False  # Reset state
        except:
            rospy.set_param("/lidar_camera_reset",1 )

rospy.init_node("warning_listener", anonymous=True)

# Initialize Publisher after node starts
pub = rospy.Publisher("lidar_status1", String, queue_size=10)
pub1 = rospy.Publisher("camera_status1", String, queue_size=10)

# Subscribe to ROS logs
rospy.Subscriber("/rosout", Log, callback)

rospy.spin()
