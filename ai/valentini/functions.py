import pickle
import os.path
from ai.model.complaint_input import ComplaintInput


async def analyze_with_valentini(complaint_input: ComplaintInput):
    result = ''
    local_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(local_path, "models/valentini.pkl")
    with open(path, 'rb') as file:
        model = pickle.load(file)
        predictions = model.predict(list(f"{complaint_input.title}. {complaint_input.description}"))
        result = predictions[0]
    return result

