from pydantic import BaseModel


class ComplaintInput(BaseModel):
    title: str
    description: str | None = None
