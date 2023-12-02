import motor.motor_asyncio

MONGO_DETAILS = "mongodb://admin:admin@localhost:27017/?authMechanism=DEFAULT"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.valentini


def get_analysis_collection():
    return database.get_collection("analysis_collection")


def get_classification_collection():
    return database.get_collection("classification_collection")


def get_ai_commands_collection():
    return database.get_collection("ai_commands_collection")


def analysis_helper(analysis) -> dict:
    return {
        "id": str(analysis["_id"]),
        "analyser": analysis["analyser"],
        "timestamp": analysis["timestamp"],
        "classification": analysis["classification"],
        "complaint_id": analysis["complaint_id"],
        "complaint_title": analysis["complaint_title"],
        "complaint_description": analysis["complaint_description"]
    }


def ai_commands_helper(command) -> dict:
    return {
        "id": str(command["_id"]),
        "name": command["name"],
        "text_command": command["text_command"]
    }


def classification_helper(command) -> dict:
    return {
        "dash_id": command["dash_id"],
        "description": command["description"]
    }


