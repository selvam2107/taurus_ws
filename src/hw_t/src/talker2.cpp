bool GlobalPlanner::makePlan(const geometry_msgs::PoseStamped& start, const geometry_msgs::PoseStamped& goal, std::vector<geometry_msgs::PoseStamped>& plan) {
    // Clear the existing plan
    plan.clear();

    // Generate an 'S' shaped path with obstacle avoidance
    generateSPathWithObstacleAvoidance(start, goal, plan);

    return true;
}

void GlobalPlanner::generateSPathWithObstacleAvoidance(const geometry_msgs::PoseStamped& start,
                                                       const geometry_msgs::PoseStamped& goal,
                                                       std::vector<geometry_msgs::PoseStamped>& plan) {
    // Define intermediate points for 'S' shape
    double mid_x = (start.pose.position.x + goal.pose.position.x) / 2.0;
    double mid_y = (start.pose.position.y + goal.pose.position.y) / 2.0;

    double t = 0.0;
    double dt = 0.1; // Adjust this value based on desired resolution

    while (t <= 1.0) {
        geometry_msgs::PoseStamped path_pose;
        path_pose.pose.position.x = mid_x + 0.5 * (goal.pose.position.x - start.pose.position.x) * (1.0 - cos(M_PI * t));
        path_pose.pose.position.y = mid_y + 0.5 * (goal.pose.position.y - start.pose.position.y) * (sin(M_PI * t));

        if (!isCollision(path_pose.pose.position)) {
            // No collision, add the pose to the plan
            path_pose.pose.orientation = tf::createQuaternionMsgFromYaw(getAngle(path_pose.pose.position, goal.pose.position));
            plan.push_back(path_pose);
        } else {
            // Handle collision by re-planning or adjusting path
            // Implement appropriate obstacle avoidance strategy
            // You might need to use a local planner here
        }

        t += dt;
    }

    // Add goal pose to the plan
    plan.push_back(goal);
}

bool GlobalPlanner::isCollision(const geometry_msgs::Point& point) {
    // Implement collision checking logic here using sensor data
    // Return true if there's a collision, false otherwise
    return false; // Placeholder implementation
}
