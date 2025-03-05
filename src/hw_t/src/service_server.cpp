#include "ros/ros.h"
#include "hw_t/Addtwoints.h"
#include <cstdlib>
bool add(hw_t::Addtwoints::Request &req,
learn_tutorials::Addtwoints::Response &res)
{   int a=23,b=45;
    res.sum=req.a+req.b;
    ROS_INFO("request: x=%ld,y=%ld",(long int) req.a,(long int) req.b);
    ROS_INFO("response: %ld",(long int) res.sum);
    return true;
}
int main(int argc,char **argv){
    ros::init(argc,argv,"add_twoints");
    ros::NodeHandle h;
    ros::ServiceServer service = h.advertiseService("add_two_ints", add);
    ROS_INFO("ready to add ints");
    ros::spin();
    return 0;

}