from fastapi import APIRouter
from pydantic import BaseModel

from app.graph.rag import workflow


router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    question: str


@router.post("/run")
def initiate_self_rag(payload: ChatRequest):

    initial_state = {
        "question": payload.question
    }

    result = workflow.invoke(
        initial_state,
        config={"recursion_limit": 80}
    )

    return {"response": result}