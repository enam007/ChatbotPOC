from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from src.core.models.room import Room, PromptInput,TasksOutput,MoodboardOutput,FilePlaceholderOutput, TasksWithDescriptionOutput

class ChatbotState(TypedDict):
    """
    Graph State For Chatbot pipeline.
    """
    messages: Annotated[list, add_messages]
    prompt: str