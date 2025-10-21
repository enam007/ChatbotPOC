from fastapi import APIRouter, HTTPException

from src.core.chat.chat_service import ChatService
from src.core.models.chat_model import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/api/ai-service/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    if not req.session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
    if not req.message or req.message.strip() == "":
        raise HTTPException(status_code=400, detail="message is required")
    session_id = req.session_id

    chat_service = ChatService(
        provider=req.provider,
        llm_name=req.llm_name,
        limit=req.limit
    )

    response_text = await chat_service.chat(session_id=session_id, user_message=req.message,task_name=req.task_name, initial_prompt=req.initial_prompt, task_description=req.task_description)
    cleaned = response_text.encode("utf-8", errors="ignore").decode("utf-8")
    return ChatResponse(session_id=session_id, response=cleaned)
