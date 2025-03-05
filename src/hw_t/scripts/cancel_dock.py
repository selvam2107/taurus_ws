import rospy
import actionlib
from hw_t.msg import aruco_detectAction,aruco_detectGoal

def cancel_goal():
    rospy.init_node('cancel_goal_client')
    client = actionlib.SimpleActionClient('Table_dock', aruco_detectAction)

    rospy.loginfo("Waiting for action server to start...")
    client.wait_for_server()

    # rospy.loginfo("Sending goal and waiting...")
    # # Optionally, send a goal before canceling
    goal = aruco_detectGoal()
    client.send_goal(goal)
    goal.detect = 0

    # rospy.sleep(5)  # Wait for some time before canceling
    # rospy.loginfo("Canceling goal...")
    client.cancel_goal()

    rospy.loginfo("Goal canceled.")

if __name__ == '__main__':
    try:
        cancel_goal()
    except rospy.ROSInterruptException:
        pass
