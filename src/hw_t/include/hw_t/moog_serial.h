#include "ros/ros.h"
#include "serial/serial.h"
#include <sstream>
#include <string>
#include <boost/algorithm/string.hpp>


class Moog{

    public:
        Moog();
        ~Moog();
        void writeMotor(int motor, std::string command);
        int readMotor(int motor, std::string command);
        void setEncoder(int motor, int value);
        void setSpeed(int motor, double velocity);
        double getEncoder(int motor);
        double getSpeed(int motor);
        void setNodeHandle(ros::NodeHandle& nh);

    private:
        ros::NodeHandle nh1;
        serial::Serial my_serial;
        std::string port="/dev/ttyUSB0";
        ulong baud=9600;
        void init();
        int encoder[2]={0,0};
        int getTraj();
};