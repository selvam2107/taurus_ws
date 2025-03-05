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

        const modelDataValue = await session.readVariableValue(nodeId);
        const fullArray = modelDataValue.value.value;

        console.log("Current Values:", fullArray);

        if (fullArray.length > 10) {
            while (true) {
                const startProgramInput = await getUserInput("\nDo you want to start the program? (yes/no): ");
                if (startProgramInput.toLowerCase() === "yes") {
                    console.log("Starting the program...");

                    console.log("Toggling index 4...");
                    fullArray[4] = 1;
                    await writeValue(nodeId, fullArray, session);
                    console.log("Index 4 set to 1.");

                    await new Promise((resolve) => setTimeout(resolve, 1000)); 

                    fullArray[4] = 0;
                    await writeValue(nodeId, fullArray, session);
                    console.log("Index 4 set back to 0.");

                    console.log("Toggling index 6...");
                    fullArray[6] = 0;
                    await writeValue(nodeId, fullArray, session);
                    console.log("Index 6 set to 0.");

                    await new Promise((resolve) => setTimeout(resolve, 1000)); 

                    fullArray[6] = 1;
                    await writeValue(nodeId, fullArray, session);
                    console.log("Index 6 set back to 1.");

                    fullArray[10] = 0;
                    await writeValue(nodeId, fullArray, session);
                    console.log("Index 10 set to 0.");
                } else if (startProgramInput.toLowerCase() === "no") {
                    console.log("Exiting program...");
                    break;
                } else {
                    console.log("Invalid input. Please enter 'yes' or 'no'.");
                    continue;
                }

                const continueTaskInput = await getUserInput("\nDo you want to continue the next task? (yes/no): ");
                if (continueTaskInput.toLowerCase() === "yes") {
                    console.log("Continuing the next task...");

                    fullArray[10] = 1;
                    await writeValue(nodeId, fullArray, session);
                    console.log("Index 10 set to 1.");
                } else if (continueTaskInput.toLowerCase() === "no") {
                    console.log("Exiting program...");
                    break;
                } else {
                    console.log("Invalid input. Please enter 'yes' or 'no'.");
                }
            }
        } else {
            console.log("Index 10 is out of range.");
        }

        await session.close();
        await client.disconnect();
        console.log("Disconnected from OPC UA Server.");
    } catch (err) {
        console.error("An error occurred:", err);
    }
}

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

connectToRobot();
