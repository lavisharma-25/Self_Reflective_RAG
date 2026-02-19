from pydantic import BaseModel, Field
from typing import List, TypedDict, Literal
from langchain_core.documents import Document

# Graph State
class State(TypedDict):
    question: str
    need_retrieval: bool
    docs: List[Document]
    answer: str

class RetrieveDecision(BaseModel):
    should_retrieve: bool = Field(
        ...,
        description="True if external documents are needed to answer reliably, else False."
    )