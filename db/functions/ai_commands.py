from db.server.database import get_ai_commands_collection, ai_commands_helper


async def retrieve_command_by(name: str) -> dict:
    command = await get_ai_commands_collection().find_one({"name": name})
    if command:
        return ai_commands_helper(command)
