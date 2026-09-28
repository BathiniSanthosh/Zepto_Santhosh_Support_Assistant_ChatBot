from pydantic import BaseModel
from typing import List

print("Loading models.py")


class QueryRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float