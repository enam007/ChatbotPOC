from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
from enum import Enum

class IntentEnum(str, Enum):
    FILTER = "Filter"
    SORT = "Sort"

class ChatbotState(TypedDict):
    """
    Graph State For Chatbot pipeline.
    """
    messages: Annotated[list, add_messages]
    prompt: str

class AgentState(TypedDict):
    """
    Graph State For Agent pipeline.
    """
    prompt: str
    intent : str
    final_response: str

class IntentOutput(BaseModel):
    intent: IntentEnum   = Field(..., description="Intent title classified from user prompt.")