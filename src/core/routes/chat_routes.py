from fastapi import APIRouter, HTTPException

from src.core.chat.chat_service import ChatService
from src.core.graph.graph import SupervisorGraph
from src.core.LLM.llm_client import LLMFactory
#from src.core.models.chat_model import ChatRequest, ChatResponse
from src.core.models.chief_of_staff_model import ChatInput, ChatOutput
#from src.core.state.memory import memory,setup_memory
from src.core.chat.chat_service import ChatService


router = APIRouter()
llm_factory = LLMFactory()
@router.post("/api/ai-service/chief-of-staff/chat", response_model=ChatOutput)
async def chat_endpoint(req: ChatInput):
    if not req.session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
    if not req.message or req.message.strip() == "":
        raise HTTPException(status_code=400, detail="message is required")
    if not req.auth_token or req.auth_token.strip() == "":
        raise HTTPException(status_code=400, detail="auth_token is required")
    session_id = req.session_id
    # global memory
    # if memory is None:
    #     memory = await setup_memory()
    llm = llm_factory.get_llm_model(provider=req.provider, llm_name=req.llm_name)
    graph  = SupervisorGraph(llm, req.auth_token).get()
    #graph = supervisor_graph.get()
    try:
        result = await graph.ainvoke(

            {"messages": [{"role": "user", "content": req.message}],
             "prompt": req.message,
             "user_id": session_id,},
            config={"configurable": {"session_id": session_id,"thread_id": session_id}},
        )
    except Exception as ex:
        raise HTTPException(500, f"Error invoking agent: {ex}")
    print("🏁 Chief of Staff final graph result:", result)
    final_response = (
        result.get("final_response")
        or (result.get("messages")[-1].get("content") if result.get("messages") else "")
    )

    return ChatOutput(
        session_id=session_id,
        response=final_response,
        intent=result.get("intent", "unknown"),
       
    )

