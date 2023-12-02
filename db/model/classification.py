from pydantic import BaseModel, Field


class ClassificationSchema(BaseModel):
    dash_id: int = Field(...)
    description: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "dash_id": 1,
                "description": "Economia"
            }
        }

