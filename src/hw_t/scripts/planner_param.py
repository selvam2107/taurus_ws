import rospy
from std_msgs.msg import String
from dynamic_reconfigure.client import Client
import yaml
def switch_planner(planner_name, param_file):
    # 1. Dynamically reconfigure the planner
    rospy.set_param('/move_base/base_local_planner', planner_name)
    
    # 2. Load and apply the parameter file
    # Assuming `param_file` is the path to the parameter file for the new planner
    # You may need to adjust this part based on how parameter files are loaded in your setup
    with open(param_file, 'r') as file:
        params = yaml.load(file, Loader=yaml.FullLoader)
        print("param uploaded",planner_name)
        rospy.set_param('/move_base/' + planner_name, params)

def main():
    print('ewd')
    rospy.init_node('planner_switcher')
    
    # Initialize dynamic reconfigure client
    client = Client("/move_base")

    def switch_planner_callback(msg):
        planner_name = msg.data
        param_file=0
        # Assuming each planner has its parameter file named after the planner
        if planner_name== 'teb':
            param_file = '/home/taurus1/testbot_ws/src/hw_t/config/teb_local_planner_param' + '.yaml'
        elif planner_name == 'dwa':
            param_file='/home/taurus1/testbot_ws/src/hw_t/config/dwa_local_planner_param' + '.yaml'

        # Switch planner and load parameters
        switch_planner(planner_name, param_file)

    rospy.Subscriber('/desired_local_planner', String, switch_planner_callback)
    
    rospy.spin()

if __name__ == '__main__':
    while True:
        main()
