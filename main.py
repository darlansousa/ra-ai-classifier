import os
from fastapi import FastAPI, HTTPException

from ai.model.complaint_input import ComplaintInput
from ai.openai.functions import analyze

from ai.routes.analysis import router as AnalysisRouter
from db.functions.analysis import retrieve_analysis, retrieve_all_analysis
from db.model.response import ResponseModel

app = FastAPI()

app.include_router(AnalysisRouter, tags=["Analysis"], prefix="/analysis")


@app.get("/", tags=["Classifier"])
async def read_root():
    return {"message": "Welcome to this fantastic classifier!"}


@app.get("/analysis", response_description="get All analysis")
async def get_all_analysis_data():
    analysis = await retrieve_all_analysis()
    return ResponseModel(analysis, "All analysis.")


@app.get("/analysis/{id}", response_description="get analysis")
async def get_analysis_data_by(id: str):
    analysis = await retrieve_analysis(id)
    return ResponseModel(analysis, "Analysis")


@app.post("/classify/{method}")
async def classify(method: str, complaint_input: ComplaintInput):
    if complaint_input.title is None or complaint_input.description is None:
        raise HTTPException(status_code=404, detail="Invalid body")
    if method == "chat-gpt":
        category = await analyze(complaint_input)
        return {
            "analyzed_item": {
                "id": f"{complaint_input.id}",
                "title": f"{complaint_input.title}",
                "description": f"{complaint_input.description}"
            },
            "category": f"{category}",
            "method": f"{method}",
            "model": f"{os.getenv('OPENAI_API_MODEL')}"
        }

    raise HTTPException(status_code=404, detail="Method not found")
