from pydantic import BaseModel, Field


class AICommandSchema(BaseModel):
    name: str = Field(...)
    text_command: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "1",
                "text_command": "Do it"
            }
        }

