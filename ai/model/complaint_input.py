from pydantic import BaseModel


class ComplaintInput(BaseModel):
    id: str
    title: str
    description: str | None = None
