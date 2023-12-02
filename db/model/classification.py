from pydantic import BaseModel, Field


class ClassificationSchema(BaseModel):
    dash_id: int = Field(...)
    name: str = Field(...)
    description: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "dash_id": 1,
                "name": "economia",
                "description": "Economia"
            }
        }

