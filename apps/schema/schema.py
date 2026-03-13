from pydantic import BaseModel, Field
from typing import List, TypedDict, Literal
from langchain_core.documents import Document

# Graph State
class State(TypedDict):
    question: str
    answer: str
    context: str

    need_retrieval: bool

    docs: List[Document]
    relevant_docs: List[Document]

    # Post Generation verification
    issup: Literal["fully_supported", "partially_supported", "no_support"]
    evidence: List[str]

    retries: int

    isuse: Literal["useful", "not_useful"]
    use_reason: str

    retrieval_query: str
    rewrite_max_retries: int

    web_query: str
    web_max_retries: int


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


class IsSUPDecision(BaseModel):
    issup: Literal["fully_supported", "partially_supported", "no_support"]
    evidence: List[str] = Field(default_factory=list)


class IsUSEDecision(BaseModel):
    isuse: Literal["useful", "not_useful"]
    reason: str = Field(..., description="Short reason in 1 line.")


class RewriteDecision(BaseModel):
    retrieval_query: str = Field(
        ...,
        description="Rewritten query optimized for vector retrieval against internal company PDFs."
    )


class WebQuery(BaseModel):
    web_query: str