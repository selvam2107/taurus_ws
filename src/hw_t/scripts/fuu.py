import pymongo

myclient = pymongo.MongoClient("mongodb://192.168.5.6:27017")
db=myclient["Running_status"]
print("created")

col=db["taurus_distance"]
i=int(input("enter:"))
col.insert_one({"_id":i})

col.update_one({"_id":i},{"$set": { "wheel1_distance": 6,"wheel2_distance":8,"total_distance":45}})
DWAPlannerROS:

# Robot Configuration Parameters
  max_vel_x: 0.5
  min_vel_x: -0.5

  max_vel_y: 0.0
  min_vel_y: 0.0


# The velocity when robot is moving in a straight line
  max_vel_trans:  0.4
  min_vel_trans:  0.01

  max_vel_theta: 0.4
  min_vel_theta: 0.01

  acc_lim_x: 4.0
  acc_lim_y: 0.0
  acc_lim_theta: 4.0


# Goal Tolerance Parameters
  xy_goal_tolerance: 0.1
  yaw_goal_tolerance: 0.1
  latch_xy_goal_tolerance: true

# Forward Simulation Parameters
  sim_time: 2.0
  vx_samples: 20
  vy_samples: 0
  vth_samples: 40
  controller_frequency: 5.0

# Trajectory Scoring Parameters
  path_distance_bias: 20.0
  goal_distance_bias: 25.0
  occdist_scale: 0.01
  forward_point_distance: 0.25
  stop_time_buffer: 0.2
  scaling_speed: 0.25
  max_scaling_factor: 0.2

# Oscillation Prevention Parameters
  oscillation_reset_dist: 0.5

# Debugging
  publish_traj_pc : true
  publish_cost_grid_pc: true

