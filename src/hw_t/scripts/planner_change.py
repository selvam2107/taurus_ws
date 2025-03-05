import rospy
from std_msgs.msg import String
from dynamic_reconfigure.client import Client

def switch_planner_callback(msg, client):
    # Determine which local planner to switch to based on the received message
    if msg.data == "dwa":
        planner_name = "dwa_local_planner/DWAPlannerROS"
    elif msg.data == "teb":
        planner_name = "teb_local_planner/TebLocalPlannerROS"
    else:
        rospy.logwarn("Unknown local planner type: %s" % msg.data)
        return

    # Dynamically reconfigure the local planner
    params = {'base_local_planner': planner_name}
    try:
        client.update_configuration(params)
        rospy.loginfo("Switched to %s" % planner_name)
    except Exception as e:
        rospy.logerr("Failed to switch planner: %s" % str(e))

def main():
    rospy.init_node('local_planner_switcher')
    
    # Initialize the dynamic reconfigure client
    try:
        client = Client("/move_base")
    except rospy.ServiceException as e:
        rospy.logerr("Failed to initialize dynamic reconfigure client: %s" % str(e))
        return

    # Subscribe to a topic that indicates the desired local planner
    rospy.Subscriber('/desired_local_planner', String, switch_planner_callback, client)

    rospy.spin()

if __name__ == '__main__':
    main()
