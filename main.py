from fastapi import FastAPI

from ai.model.complaint_input import ComplaintInput

app = FastAPI()


@app.get("/")
async def root():
    return "RA AI Classifier"


@app.post("/classify/{method}")
async def classify(method: str, complaint_input: ComplaintInput):
    return {
        "method": f"{method}",
        "title": f"{complaint_input.title}",
        "description": f"{complaint_input.description}"
    }
