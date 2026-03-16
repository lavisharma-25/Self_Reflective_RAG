from typing import List, TypedDict, Literal
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage


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

    chat_history: List[BaseMessage]
