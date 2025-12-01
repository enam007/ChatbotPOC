from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    A standard interface for all agent classes.
    Child classes must implement build() to return a LangGraph agent instance.
    """

    def __init__(self, llm, auth_token=None):
        self.llm = llm
        self.auth_token = auth_token
        self.tools = {}
        self.agent = None

    @abstractmethod
    def build(self):
        """Return the constructed agent"""
        ...
