const opcua = require("node-opcua");

const endpointUrl = "opc.tcp://192.168.7.60:4880";

const client = opcua.OPCUAClient.create({ endpointMustExist: false });

async function connectToRobot() {
    try {
        await client.connect(endpointUrl);
        console.log("Connected to OPC UA Server at:", endpointUrl);

        const session = await client.createSession();
        console.log("Session created.");

        const nodeId = "ns=1;i=304";

        console.log("Monitoring index 22...");
        while (true) {
            // Read the current value
            const modelDataValue = await session.readVariableValue(nodeId);
            const fullArray = modelDataValue.value.value;

            if (fullArray.length > 22) {
                const index22 = fullArray[22]; // Get the value at index 22

                if (index22 === 1) {
                    console.log("Program is Running");
                } else if (index22 === 0) {
                    console.log("Program is Stopped");
                } else {
                    console.log(`Unexpected value at index 22: ${index22}`);
                }
            } else {
                console.error("Index 22 is out of range.");
            }

            await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait 1 second before next read
        }
    } catch (err) {
        console.error("An error occurred:", err);
    } finally {
        await client.disconnect();
        console.log("Disconnected from OPC UA Server.");
    }
}

// Start the program
connectToRobot();

