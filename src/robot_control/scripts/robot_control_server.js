const rosnodejs = require('rosnodejs');
const actionlib = rosnodejs.require('actionlib');
const { RobotControlAction, RobotControlFeedback, RobotControlResult } = rosnodejs.require('robot_control_msgs').action;

function main() {
  rosnodejs.initNode('/robot_control_server').then((rosNode) => {
    // Create an ActionServer to handle RobotControlAction
    const server = new actionlib.ActionServer({
      nh: rosNode,
      type: RobotControlAction,
      actionServer: '/robot_control',
    });

    console.log('Action server started for /robot_control');

    // Register a callback to handle incoming goals
    server.registerGoalCallback((goalHandle) => {
      console.log('Received goal:', goalHandle.getGoal());

      const command = goalHandle.getGoal().command;
      const feedback = new RobotControlFeedback();
      const result = new RobotControlResult();

      // Process based on the command
      if (command === 1) {
        feedback.status = 'Starting robot';
        goalHandle.publishFeedback(feedback);
        console.log('Robot is starting...');

        // Simulate a delay for starting the robot
        setTimeout(() => {
          result.result = 'Robot started successfully';
          goalHandle.setSucceeded(result);
          console.log('Robot started successfully.');
        }, 2000);
      } else if (command === 2) {
        feedback.status = 'Moving robot';
        goalHandle.publishFeedback(feedback);
        console.log('Robot is moving...');

        setTimeout(() => {
          result.result = 'Robot moved successfully';
          goalHandle.setSucceeded(result);
          console.log('Robot moved successfully.');
        }, 3000);
      } else if (command === 3) {
        feedback.status = 'Stopping robot';
        goalHandle.publishFeedback(feedback);
        console.log('Robot is stopping...');

        setTimeout(() => {
          result.result = 'Robot stopped successfully';
          goalHandle.setSucceeded(result);
          console.log('Robot stopped successfully.');
        }, 1000);
      } else {
        // Invalid command
        result.result = `Invalid command: ${command}`;
        goalHandle.setRejected(result);
        console.log('Goal rejected: Invalid command');
      }
    });

    // Register a callback to handle cancellation of goals
    server.registerCancelCallback((goalHandle) => {
      console.log('Goal canceled:', goalHandle.getGoalId());
      goalHandle.setCanceled();
    });
  });
}

main();
