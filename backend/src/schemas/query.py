from pydantic import BaseModel, ConfigDict

class QueryRequest(BaseModel):
    question: str
    context: str

class QueryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    answer: str
    sources: list[str]
    confidence: float
    related_topic: list[str]