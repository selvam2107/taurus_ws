const opcua = require("node-opcua");
const redis = require("redis");

const endpointUrl = "opc.tcp://192.168.7.60:4880";

const redisClient = redis.createClient({
    url: "redis://192.168.5.7:6379"
});

redisClient.on("connect", () => {
    console.log("Connected to Redis server on localhost.");
});

redisClient.on("error", (err) => {
    console.error("Redis error:", err);
});

const client = opcua.OPCUAClient.create({ endpointMustExist: false });

async function connectToRobot() {
    try {
        await redisClient.connect();
        console.log("Redis client connected.");

        await client.connect(endpointUrl);
        console.log("Connected to OPC UA Server at:", endpointUrl);

        const session = await client.createSession();
        console.log("Session created.");

        const nodeId = "ns=1;i=304";

        const modelDataValue = await session.readVariableValue(nodeId);
        let fullArray = modelDataValue.value.value;

        console.log("Initial Values:", fullArray);

        fullArray[6] = 0;
        await writeValue(nodeId, fullArray, session);
        console.log("Index 6 set to 0.");
        await new Promise((resolve) => setTimeout(resolve, 1000));

        fullArray[6] = 1;
        await writeValue(nodeId, fullArray, session);
        console.log("Index 6 set back to 1.");

        while (true) {
            const task1 = await getRedisValue("task1");
            const task2 = await getRedisValue("task2");
            const task3 = await getRedisValue("task3");
            const task4 = await getRedisValue("task4");

            if (task1 === "go") {
                console.log("Running Task 1...");
                fullArray[10] = 1;
                await writeValue(nodeId, fullArray, session);
                console.log("Index 10 set to 1.");
                await new Promise((resolve) => setTimeout(resolve, 2000));
                fullArray[10] = 0;
                await writeValue(nodeId, fullArray, session);
                console.log("Index 10 set back to 0.");

                while (true) {
                    const updatedValue = await session.readVariableValue(nodeId);
                    fullArray = updatedValue.value.value;
                    if (fullArray[40] === 1) {
                        await setRedisValue("task1", "done");
                        fullArray[40] = 0; // Set index 40 to 1
                        await writeValue(nodeId, fullArray, session);
                        console.log("Index 40 set to 1.");
                        break;
                    }
                    await new Promise((resolve) => setTimeout(resolve, 500));
                }
            }

            if (task2 === "go") {
                console.log("Running Task 2...");
                fullArray[11] = 1;
                await writeValue(nodeId, fullArray, session);
                console.log("Index 11 set to 1.");
                await new Promise((resolve) => setTimeout(resolve, 2000));
                fullArray[11] = 0;
                await writeValue(nodeId, fullArray, session);
                console.log("Index 11 set back to 0.");

                while (true) {
                    const updatedValue = await session.readVariableValue(nodeId);
                    fullArray = updatedValue.value.value;
                    if (fullArray[40] === 1) {
                        await setRedisValue("task2", "done");
                        fullArray[40] = 0; // Set index 40 to 1
                        await writeValue(nodeId, fullArray, session);
                        console.log("Index 40 set to 1.");
                        break;
                    }
                    await new Promise((resolve) => setTimeout(resolve, 500));
                }
            }

            if (task3 === "go") {
                console.log("Running Task 3...");
                fullArray[12] = 1;
                await writeValue(nodeId, fullArray, session);
                console.log("Index 12 set to 1.");
                await new Promise((resolve) => setTimeout(resolve, 2000));
                fullArray[12] = 0;
                await writeValue(nodeId, fullArray, session);
                console.log("Index 12 set back to 0.");

                while (true) {
                    const updatedValue = await session.readVariableValue(nodeId);
                    fullArray = updatedValue.value.value;
                    if (fullArray[40] === 1) {
                        await setRedisValue("task3", "done");
                        fullArray[40] = 0; // Set index 40 to 1
                        await writeValue(nodeId, fullArray, session);
                        console.log("Index 40 set to 1.");
                        break;
                    }
                    await new Promise((resolve) => setTimeout(resolve, 500));
                }
            }

            if (task4 === "go") {
                console.log("Running Task 4...");
                fullArray[13] = 1;
                await writeValue(nodeId, fullArray, session);
                console.log("Index 13 set to 1.");
                await new Promise((resolve) => setTimeout(resolve, 2000));
                fullArray[13] = 0;
                await writeValue(nodeId, fullArray, session);
                console.log("Index 13 set back to 0.");

                while (true) {
                    const updatedValue = await session.readVariableValue(nodeId);
                    fullArray = updatedValue.value.value;
                    if (fullArray[40] === 1) {
                        await setRedisValue("task4", "done");
                        fullArray[40] = 0; // Set index 40 to 1
                        await writeValue(nodeId, fullArray, session);
                        console.log("Index 40 set to 1.");
                        break;
                    }
                    await new Promise((resolve) => setTimeout(resolve, 500));
                }
            }

            await new Promise((resolve) => setTimeout(resolve, 1000));
        }
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

function getRedisValue(key) {
    return redisClient.get(key);
}

async function setRedisValue(key, value) {
    try {
        await redisClient.set(key, value);
        console.log(`Redis key "${key}" set to "${value}".`);
    } catch (err) {
        console.error(`Error setting Redis key "${key}":`, err);
    }
}

connectToRobot();

