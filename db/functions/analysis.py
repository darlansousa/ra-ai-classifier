from bson.objectid import ObjectId

from db.server.database import get_analysis_collection, analysis_helper


async def retrieve_all_analysis():
    all_analysis = []
    async for analysis in get_analysis_collection().find():
        all_analysis.append(analysis_helper(analysis))
    return all_analysis


async def add_analysis(analysis_data: dict) -> dict:
    existent = await retrieve_analysis_by(analysis_data['complaint_id'])
    if existent:
        return existent
    analysis = await get_analysis_collection().insert_one(analysis_data)
    new_analysis = await get_analysis_collection().find_one({"_id": analysis.inserted_id})
    return analysis_helper(new_analysis)


async def retrieve_analysis(id_analysis: str) -> dict:
    analysis = await get_analysis_collection().find_one({"_id": ObjectId(id_analysis)})
    if analysis:
        return analysis_helper(analysis)


async def retrieve_analysis_by(complaint_id: str) -> dict:
    analysis = await get_analysis_collection().find_one({"complaint_id": complaint_id})
    if analysis:
        return analysis_helper(analysis)


async def update_analysis(id_analysis: str, data: dict):
    if len(data) < 1:
        return False
    analysis = await get_analysis_collection().find_one({"_id": ObjectId(id_analysis)})
    if analysis:
        updated_analysis = await get_analysis_collection().update_one(
            {"_id": ObjectId(id_analysis)}, {"$set": data}
        )
        if updated_analysis:
            return True
        return False


async def delete_analysis(id_analysis: str):
    analysis = await get_analysis_collection().find_one({"_id": ObjectId(id_analysis)})
    if analysis:
        await get_analysis_collection().delete_one({"_id": ObjectId(id_analysis)})
        return True
