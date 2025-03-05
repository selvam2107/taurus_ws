const opcua = require("node-opcua");
const readline = require("readline");

const endpointUrl = "opc.tcp://192.168.7.60:4880";

const client = opcua.OPCUAClient.create({ endpointMustExist: false });

async function connectToRobot() {
    try {
        await client.connect(endpointUrl);
        console.log("Connected to OPC UA Server at:", endpointUrl);

        const session = await client.createSession();
        console.log("Session created.");

        const nodeId = "ns=1;i=304";

        // Read the current value
        const modelDataValue = await session.readVariableValue(nodeId);
        const fullArray = modelDataValue.value.value;

        console.log("Current Values:", fullArray);

        if (fullArray.length > 18) {
            // Toggle index 4
          //  console.log("Toggling index 4...");
            fullArray[4] = 1;
            await writeValue(nodeId, fullArray, session);
          //  console.log("Index 4 set to 1 (ON).");
            await new Promise((resolve) => setTimeout(resolve, 3000)); // Wait for 3 seconds

            fullArray[4] = 0;
            await writeValue(nodeId, fullArray, session);
          //  console.log("Index 4 set to 0 (OFF).");

            // Toggle index 6
          //  console.log("Toggling index 6...");
            fullArray[6] = 0;
            await writeValue(nodeId, fullArray, session);
            await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait for 1 second

            fullArray[6] = 1;
            await writeValue(nodeId, fullArray, session);
         //   console.log("Index 6 toggled (OFF -> ON).");

            // Main program loop
            while (true) {
                console.log("\n1. Hold\n2. Release the Hold\n3. Abort");
                const userInput = await getUserInput("Enter your choice (1/2/3): ");

                if (userInput === "1") {
                    console.log("The Robot is on Hold");
                    fullArray[1] = 0;
                    await writeValue(nodeId, fullArray, session);
                    console.log("Index 1 set to 0.");
                } else if (userInput === "2") {
                    console.log("Releasing Hold...");
                    fullArray[1] = 1;
                    await writeValue(nodeId, fullArray, session);

                    fullArray[4] = 1;
                    await writeValue(nodeId, fullArray, session);
                    await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait for 1 second
                    fullArray[4] = 0;
                    await writeValue(nodeId, fullArray, session);
           //         console.log("Index 4 toggled.");
                } else if (userInput === "3") {
                    console.log("Aborting program...");
                    fullArray[18] = 1; // Turn index 18 ON
                    await writeValue(nodeId, fullArray, session);
                    console.log("Index 18 set to 1 (ON).");

                    const restartInput = await getUserInput(
                        "Do you want to run the program again? (yes/no): "
                    );

                    if (restartInput.toLowerCase() === "yes") {
                        console.log("Restarting program...");
                        fullArray[18] = 0; // Turn index 18 OFF
                        await writeValue(nodeId, fullArray, session);
                        console.log("Index 18 set to 0 (OFF).");

                        // Toggle index 6 OFF and ON
                        console.log("Toggling index 6...");
                        fullArray[6] = 0;
                        await writeValue(nodeId, fullArray, session);
                        await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait for 1 second

                        fullArray[6] = 1;
                        await writeValue(nodeId, fullArray, session);
                        console.log("Index 6 toggled.");
                    } else {
                        console.log("Exiting program...");
                        break;
                    }
                } else {
                    console.log("Invalid input. Please enter 1, 2, or 3.");
                }
            }
        } else {
            console.log("Index 4, 6, or 18 is out of range.");
        }

        await session.close();
        await client.disconnect();
        console.log("Disconnected from OPC UA Server.");
    } catch (err) {
        console.error("An error occurred:", err);
    }
}

// Function to write values to the server
async function writeValue(nodeId, array, session) {
    const writeValue = {
        nodeId: nodeId,
        attributeId: opcua.AttributeIds.Value,
        value: {
            value: {
                dataType: "Int16",
                arrayType: opcua.VariantArrayType.Array,
                value: array,
            },
        },
    };

    const statusCode = await session.write([writeValue]);
    if (statusCode[0].isGood()) {
        console.log("Write operation successful.");
    } else {
        console.log(`Write operation failed with status: ${statusCode[0].toString()}`);
    }
}

// Helper function to get user input
function getUserInput(question) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    return new Promise((resolve) => {
        rl.question(question, (answer) => {
            rl.close();
            resolve(answer.trim());
        });
    });
}

// Start the program
connectToRobot();


