from langgraph.graph import StateGraph, END
from src.core.state.state import AgentState, IntentEnum
from langgraph.checkpoint.memory import MemorySaver

from src.core.agents.filter_tool_agent import FilterAgent
from src.core.agents.sorting_agent import SortingAgent

from src.core.nodes.intent_parser_node import IntentParserNode


class SupervisorGraph:
    def __init__(self, model, auth_token):
        self.llm = model
        self.auth_token = auth_token

        filter_agent = FilterAgent(self.llm, self.auth_token).build()
        sorting_agent = SortingAgent(self.llm, self.auth_token).build()

        # ---------- INTENT ROUTER ----------
        def route_after_intent(state: AgentState):
            intent = state.get("intent")

            if intent == IntentEnum.FILTER:
                return "filter_agent"

            if intent == IntentEnum.SORT:
                return "sorting_agent"

            # safety fallback
            return END

        # ---------- GRAPH ----------
        intent_node = IntentParserNode(self.llm)

        workflow = StateGraph(AgentState)

        workflow.add_node("intent_node", intent_node)
        workflow.add_node("filter_agent", filter_agent)
        workflow.add_node("sorting_agent", sorting_agent)

        workflow.set_entry_point("intent_node")

        # Conditional routing based on parsed intent
        workflow.add_conditional_edges(
            "intent_node",
            route_after_intent,
            {
                "filter_agent": "filter_agent",
                "sorting_agent": "sorting_agent",
                END: END,
            },
        )

        # End points for both agents
        workflow.add_edge("filter_agent", END)
        workflow.add_edge("sorting_agent", END)

        self.graph = workflow.compile(checkpointer=MemorySaver())

    def get(self):
        return self.graph
