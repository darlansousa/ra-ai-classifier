import os
from fastapi import FastAPI


from ai.model.complaint_input import ComplaintInput
from ai.openai.functions import analyze

app = FastAPI()


@app.get("/")
async def root():
    return "RA AI Classifier"


@app.post("/classify/{method}")
async def classify(method: str, complaint_input: ComplaintInput):
    if method == "chat-gpt":
        category = await analyze(complaint_input)
        return {
            "analyzed_item": {
                "title": f"{complaint_input.title}",
                "description": f"{complaint_input.description}"
            },
            "category": f"{category}",
            "method": f"{method}",
            "model": f"{os.getenv('OPENAI_API_MODEL')}"
        }

    return {
        "method": f"{method}",
        "title": f"{complaint_input.title}",
        "description": f"{complaint_input.description}"
    }

