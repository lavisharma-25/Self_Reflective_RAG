from fastapi import APIRouter
from pydantic import BaseModel

from app.graph.rag import workflow
from app.models.schema import ChatRequest

router = APIRouter(prefix="/chat", tags=["Chat"])

chat_sessions = {}

@router.post("/run")
def initiate_self_rag(request: ChatRequest):

    session_id = request.session_id

    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    state = {
        "question": request.question,
        "chat_history": chat_sessions[session_id],
    }

    result = workflow.invoke(state)

    chat_sessions[session_id] = result["chat_history"][-20:]

    return {"response": result}