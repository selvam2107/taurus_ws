// Import ROSLIB
const ROSLIB = require('roslib');

// Initialize ROS connection
const ros = new ROSLIB.Ros({
    url: 'ws://localhost:9090' // Ensure this matches your ROS bridge WebSocket address
});

// Log connection status
ros.on('connection', function () {
    console.log('Connected to ROS.');
});

ros.on('error', function (error) {
    console.error('Error connecting to ROS:', error);
});

ros.on('close', function () {
    console.log('Connection to ROS closed.');
});

// Function to update and publish the footprint
function updateAndPublishFootprint() {
    // Set the updated footprint
    const updatedFootprint = [
        [-0.105, -0.105],
        [-0.105, 0.105],
        [0.041, 0.105],
        [0.041, -0.105]
    ];

    // Set the footprint as a parameter
    const param = new ROSLIB.Param({
        ros: ros,
        name: '/robot_config/footprint'
    });

    param.set(updatedFootprint, function () {
        console.log('Updated footprint set in parameter server:', updatedFootprint);
    });

    // Create the Polygon message
    const footprintMsg = {
        points: updatedFootprint.map(([x, y]) => ({ x, y, z: 0 }))
    };

    // Publisher for the footprint topic
    const footprintPub = new ROSLIB.Topic({
        ros: ros,
        name: '/move_base/local_costmap/footprint',
        messageType: 'geometry_msgs/Polygon'
    });

    // Function to publish the footprint at a regular interval
    function publishFootprint() {
        footprintPub.publish(new ROSLIB.Message(footprintMsg));
        console.log('Published updated footprint to /move_base/local_costmap/footprint');
    }

    // Publish the footprint every second
    setInterval(publishFootprint, 1000);
}

// Call the function to start updating and publishing the footprint
updateAndPublishFootprint();


