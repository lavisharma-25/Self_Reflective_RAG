from pydantic import BaseModel, Field
from typing import List, TypedDict, Literal
from langchain_core.documents import Document

# Graph State
class State(TypedDict):
    question: str
    answer: str

    need_retrieval: bool

    docs: List[Document]
    relevant_docs: List[Document]


class RetrieveDecision(BaseModel):
    should_retrieve: bool = Field(
        ...,
        description="True if external documents are needed to answer reliably, else False."
    )


class RelevanceDecision(BaseModel):
    is_relevant: bool = Field(
        ...,
        description="True if the document helps answer the question, else False."
    )