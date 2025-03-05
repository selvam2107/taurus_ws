#include "hw_t/moons_client.h"
#include <typeinfo>


Moons::Moons(){

  std::cout<<"Moons object created\n";
  init();
}

Moons::~Moons()
{
  std::cout<<"****************Destruction of Moons class done*************************\n";
}

void Moons::init(){

  // if(my_serial.isOpen())
  //     std::cout << "Serial connection: Yes." << std::endl;    
  //   else
  //     std::cout << "serial connection: No." << std::endl;

  // std::cout<<"Serial port: " <<my_serial.getPort()<<"\n";


    // writeMotor(0, "ECHO\rADT=500\rMV\rZS");    
    
  // writeMotor(0, "O=0");
}

void Moons::setNodeHandle(ros::NodeHandle& nh){
  this->nh1=nh;
}


//--------------------------------------------------------------------------------------

void Moons::writeMotor(short int motor,short int entity, long int value1, long int value2){
  //Enter motor number, entity =1(encoder)and2(speed), value
  
  short int result=9;
  // value1 = -value1;
  // value2 = value2;
  
  // std::cout<<"Writing to motor "<<motor<<" Command: "<<command<<"\n";
  write_srv.request.motor=motor;
  write_srv.request.entity=entity;
  write_srv.request.value1=value1;
  write_srv.request.value2=value2;
  // ROS_INFO("writeMotor: int motor= %d, short int entity= %hi, long int value= %ld",motor, entity, value);
  std::cout<<"---------Moons::writeMotor---------------\n";
  ROS_INFO("speed1= %ld\tspeed2= %ld", value1, value2);

  if (write_client.call(write_srv)){
      result= write_srv.response.result;
  }
  else if(result==9){
    ROS_WARN("server returned error, check the server program");
  }

  result=9;
  
  switch (result)
  {
  case 0:
    ROS_INFO("Motor is not connected");
    break;
  case 1:
    break;
  case 9:
    break;
  default:
  ROS_INFO("unknown result; result: %hi", result);
    break;
  }
}

taurusData Moons::readMotor(double prev1, double prev2){
  //Enter motor number and read command like RPA or RVA

  short int result;
  taurusData value;
  
  // std::cout<<"Writing to motor "<<motor<<" Command: "<<command<<"\n";
  read_srv.request.prev1=(long int)prev1;
  read_srv.request.prev2=(long int)prev2;
  if (read_client.call(read_srv)){
      result= read_srv.response.result;
      value.enc1= (double) read_srv.response.enc1;
      value.enc2=(double) read_srv.response.enc2;
      value.vel1=(double) read_srv.response.vel1;
      value.vel2=(double) read_srv.response.vel2;

  }
  else{
    ROS_WARN("Server is not hosted; run 'rosrun rcpp moons_server.py'");
    // value=0;
  }

  switch (result)
  {
  case 0:
    ROS_INFO("Motor is not connected");
    break;
  case 1:
    break;
  case 2:
    ROS_ERROR("Invalid entity in write function");
    throw ("enter valid entity");
    break;
  default:
    ROS_INFO("unknown result; result: %hi", result);
    // value=0;
    break;
  }
  return value;
}

// -------------------------------------------------------------------------------------

// TODO:
void Moons::setEncoder(short int motor_add,double enc1, double enc2){
  // input direct int Encoder value
  
  // writeMotor(motor, "O="+std::to_string(value));
}

void Moons::setSpeed(short int motor_add, double vel1, double vel2){
  // input velocity is in degrees per second
  // int x;
	// x=(int) round((velocity/360)*65536*25);
  // writeMotor(motor, "VT="+std::to_string(x)+"\rG");
  long int deg1,deg2;
  int gear_ratio=40 ;
  deg1= round((vel1/360)*240*gear_ratio);
  deg2=round((vel2/360)*240*gear_ratio);
  deg1 = deg1;
  deg2 = deg2;
  // ROS_INFO("setSpeed: int motor= %d, double velocity= %lf, long int deg= %ld",motor, velocity, deg);
  writeMotor(motor_add,2, deg1,deg2);
}

taurusData Moons::getData(){
  taurusData data;
  int gear_ratio=40;
  data=readMotor(encoder[0],encoder[1]);
  encoder[0]=data.enc1;
  encoder[1]=data.enc2;
  data.enc1 = data.enc1;
  data.enc2 = data.enc2;
  
  data.enc1=(data.enc1*360)/(10000*gear_ratio);
  data.enc2=(data.enc2*360)/(10000*gear_ratio);
  data.vel1= (360*data.vel1)/(240*gear_ratio);
  data.vel2= (360*data.vel2)/(240*gear_ratio);
  return data;
}