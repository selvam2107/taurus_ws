const rosnodejs = require('rosnodejs');
const actionlib = rosnodejs.require('actionlib');
const { RobotControlActionGoal } = rosnodejs.require('robot_control_msgs').action;

function main() {
  rosnodejs.initNode('/robot_control_client').then((rosNode) => {
    // Create an ActionClient to connect to the ActionServer
    const actionClient = new actionlib.ActionClient({
      ros: rosNode,
      serverName: '/robot_control',
      actionType: RobotControlActionGoal,
    });

    const command = parseInt(process.argv[2]);

    // Validate command argument
    if (![1, 2, 3].includes(command)) {
      console.log('Invalid command! Use 1, 2, or 3.');
      return;
    }

    const goalMessage = { command: command };
    const goal = new actionlib.Goal({
      actionClient,
      goalMessage: goalMessage,
    });

    // Listen to feedback from the action server
    goal.on('feedback', (feedback) => {
      console.log('Feedback:', feedback.status);
    });

    // Listen to the result when the goal is completed
    goal.on('result', (result) => {
      console.log('Result:', result.result);
    });

    // Send the goal to the server
    console.log('Sending goal:', goalMessage);
    goal.send();
  });
}

main();
