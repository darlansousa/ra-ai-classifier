import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ai.model.complaint_input import ComplaintInput
from ai.openai.functions import analyze_with_gpt

from ai.routes.analysis import router as AnalysisRouter
from ai.valentini.functions import analyze_with_valentini
from db.functions.analysis import retrieve_all_analysis, confirm_analysis, retrieve_analysis_by
from db.model.response import ResponseModel, ErrorResponseModel

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3001",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    analysis = await retrieve_analysis_by(id)
    return ResponseModel(analysis, "Analysis")


@app.put("/analysis/{id}/confirm", response_description="get analysis")
async def patch_analysis_data_by(id: str):
    analysis = await confirm_analysis(id)
    return ResponseModel(analysis, "Analysis")


@app.post("/classify/{method}")
async def classify(method: str, complaint_input: ComplaintInput):
    if complaint_input.title is None or complaint_input.description is None:
        raise HTTPException(status_code=404, detail="Invalid body")
    if method == "chat-gpt":
        category = await analyze_with_gpt(complaint_input)
        if type(category) is TypeError:
            return ErrorResponseModel(category, "500", category)

        return {
            "analyzed_item": {
                "id": f"{complaint_input.id}",
                "title": f"{complaint_input.title}",
                "description": f"{complaint_input.description}"
            },
            "category": category,
            "method": f"{method}",
            "model": f"{os.getenv('OPENAI_API_MODEL')}"
        }

    if method == "valentini":
        category = await analyze_with_valentini(complaint_input)
        return {
            "analyzed_item": {
                "id": f"{complaint_input.id}",
                "title": f"{complaint_input.title}",
                "description": f"{complaint_input.description}"
            },
            "category": category,
            "method": "valentini",
            "model": "valentini"
        }

    raise HTTPException(status_code=404, detail="Method not found")
