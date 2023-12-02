from db.server.database import get_classification_collection, classification_helper


async def retrieve_all_classification():
    all_classification = []
    async for classification in get_classification_collection().find():
        all_classification.append(classification_helper(classification))
    return all_classification
