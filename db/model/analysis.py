from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AnalysisSchema(BaseModel):
    analyser: str = Field(...)
    timestamp: datetime = datetime.now()
    classification: str = Field(...)
    complaint_id: str = Field(...)
    complaint_title: str = Field(...)
    complaint_description: str = Field(...)
    confirmed: bool = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "analyser": "valentini",
                "timestamp": "123658989528",
                "classification": "Test",
                "complaint_id": "XGABDCRT",
                "complaint_title": "text",
                "complaint_description": "text",
                "confirmed": True
            }
        }


class InsertOrUpdateAnalysisModel(BaseModel):
    analyser: Optional[str]
    timestamp: Optional[datetime]
    classification: Optional[str]
    complaint_id: Optional[str]
    complaint_title: Optional[str]
    complaint_description: Optional[str]
    confirmed: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "analyser": "valentini",
                "timestamp": "123658989528",
                "classification": "Test",
                "complaint_id": "XGABDCRT",
                "complaint_title": "text",
                "complaint_description": "text",
            }
        }
