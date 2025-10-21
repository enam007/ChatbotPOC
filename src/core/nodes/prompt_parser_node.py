# src/langgraphengine/nodes/parser_node.py

from src.core.models.room import PromptInput
from src.core.state.state import ChatbotState
class PromptParserNode:
    def __init__(self):
        self.state = {}

    def parse(self, state: ChatbotState) -> ChatbotState:
        """
        Parse raw user prompt.
        """
        user_prompt = state["prompt"]
        parsed = PromptInput(user_prompt=user_prompt)

        state["parsed_input"] = parsed
        self.state["parsed_input"] = parsed
        return state
