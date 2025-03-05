#include "ros/ros.h"
#include <sstream>
#include <string>
#include <boost/algorithm/string.hpp>
#include "hw_t/moonsRead.h"
#include "hw_t/moonsWrite.h"

struct taurusData
{
    double enc1, enc2, vel1, vel2;
};

class Moons{

    public:
        Moons();
        ~Moons();
        void writeMotor(short int motor,short int entity, long int value1, long int value2);
        taurusData readMotor(double prev1, double prev2);

        void setEncoder(short int motor_add,double enc1, double enc2);
        void setSpeed(short int motor_add, double vel1, double vel2);
        void setData(taurusData);
        
        taurusData getData();
        void setNodeHandle(ros::NodeHandle& nh);

    private:
        ros::NodeHandle nh1;
        // CHECK:
        // This was added but functionality to be added, refer '/home/product/jana_ws/src/trial_service/src/cppclient.cpp'
        ros::ServiceClient read_client = nh1.serviceClient<hw_t::moonsRead>("moons_read");
        ros::ServiceClient write_client = nh1.serviceClient<hw_t::moonsWrite>("moons_write");
        hw_t::moonsRead read_srv;
        hw_t::moonsWrite write_srv;
        int left=2, right=1;

        void init();
        long int encoder[2]={0,0};
};