
from pydantic import BaseModel
class ChatInput(BaseModel):
    session_id: str | None = None
    message: str
    provider: str = "groq"
    llm_name: str | None = None
    auth_token: str 

class ChatOutput(BaseModel):
    session_id: str
    response: str
    intent: str 