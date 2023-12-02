import pickle
import os.path
import pandas as pd
from ai.model.complaint_input import ComplaintInput
from ai.valentini.util.functions import formatting
from db.functions.classification import retrieve_all_classification


async def filter_classification(name) -> dict:
    items = await retrieve_all_classification()
    first = None
    filtered = [item for item in items if item['name'] == name.lower()]
    if len(filtered) > 0:
        first = filtered[0]
    return first


async def analyze_with_valentini(complaint_input: ComplaintInput):
    local_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(local_path, "models/valentini.pkl")
    with open(path, 'rb') as file:
        model = pickle.load(file)
        docs_df = {'title': [complaint_input.title], 'description': [complaint_input.description]}
        docs = pd.DataFrame(data=docs_df)
        processed = formatting(docs)
        predictions = model.predict(processed.tolist())
        result = await filter_classification(predictions[0])
    return result
