#include "hw_t/hw_interface.h"
//namesapce i2c_ros
using namespace std;
Taurus::Taurus(ros::NodeHandle& nh) : nh_(nh) {
    init();
    motor.setNodeHandle(nh);

    controller_manager_.reset(new controller_manager::ControllerManager(this, nh_));
    loop_hz_=10;
    ros::Duration update_freq = ros::Duration(1.0/loop_hz_);
	
	
    non_realtime_loop_ = nh_.createTimer(update_freq, &Taurus::update, this);
}

Taurus::~Taurus() {
}

void Taurus::init() {
	
	for(int i=0; i<2; i++)
	{
	// Create joint state interface register our joints
        hardware_interface::JointStateHandle jointStateHandle(joint_name_[i], &joint_position_[i], &joint_velocity_[i], &joint_effort_[i]);
        joint_state_interface_.registerHandle(jointStateHandle);
       
    // Create velocity joint interface
	    hardware_interface::JointHandle jointVelocityHandle(jointStateHandle, &joint_velocity_command_[i]);
        velocity_joint_interface_.registerHandle(jointVelocityHandle);

    // Create Joint Limit interface   
        joint_limits_interface::JointLimits limits;
        joint_limits_interface::getJointLimits(joint_name_[i], nh_, limits);
	    joint_limits_interface::VelocityJointSaturationHandle jointLimitsHandle(jointVelocityHandle, limits);
	    velocityJointSaturationInterface.registerHandle(jointLimitsHandle);

	}
    joint_velocity_command_[0]=0;
    joint_velocity_command_[1]=0;
    
// Register all joints interfaces    
    registerInterface(&joint_state_interface_);
    registerInterface(&velocity_joint_interface_);
    registerInterface(&velocityJointSaturationInterface);
}

void Taurus::update(const ros::TimerEvent& e) {
    elapsed_time_ = ros::Duration(e.current_real - e.last_real);
    read();
    controller_manager_->update(ros::Time::now(), elapsed_time_);
    write(elapsed_time_);
}

void Taurus::read() {

    taurusData data;
    // TODO: Change getEncoder() and getSpeed() in moog_serial
    data= motor.getData();

    left_motor_pos=angles::from_degrees(data.enc1);
    joint_position_[0]=left_motor_pos;

    right_motor_pos=angles::from_degrees(data.enc2);
    joint_position_[1]=right_motor_pos;
    // -----------------------------------------------------
    left_motor_vel=angles::from_degrees(data.vel1);
    joint_velocity_[0]=left_motor_vel;
    
    right_motor_vel=angles::from_degrees(data.vel2);
    joint_velocity_[1]=right_motor_vel;

    // std::cout<<"-----"<<joint_position_[0]<<"       "<<joint_position_[1]<<"-------------\n";

    //ROS_INFO("pos=%.2f x=%d ",pos,x);
	
}

void Taurus::write(ros::Duration elapsed_time) {

    velocityJointSaturationInterface.enforceLimits(elapsed_time);   
    double vel1,vel2,result;
    short int motor_add=0;
    // motor_add: 00-> none, 01-> motor1, 10-> motor2, 11->both

    vel1=angles::to_degrees(joint_velocity_command_[0]);
    vel2=angles::to_degrees(joint_velocity_command_[1]);
	//ROS_INFO("joint_velocity_command_[0]=%.2f velocity=%d  B1=%d B2=%d", joint_velocity_command_[0],velocity,wbuff[0],wbuff[1]);
    // vel2=-vel2;
    if(left_prev_cmd!=vel1)
    {
        motor_add++;
	    left_prev_cmd=vel1;
    }
    if(right_prev_cmd!=vel2)
    {
        motor_add+=10;
	    right_prev_cmd=vel2;
    }
    if (motor_add!=0){
        motor.setSpeed(motor_add,vel1,vel2);
    }
}



int main(int argc, char** argv)
{
    ros::init(argc, argv, "mobile_robot_hardware_interface");
    ros::NodeHandle nh;
    //ros::AsyncSpinner spinner(4);  
    ros::MultiThreadedSpinner spinner(2); // Multiple threads for controller service callback and for the Service client callback used to get the feedback from ardiuno
    Taurus ROBOT(nh);
    //spinner.start();
    spinner.spin();
    //ros::spin();
    return 0;
}
