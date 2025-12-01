# src/agents/sorting_agent.py

from src.core.agents.base_agent import BaseAgent
from langgraph.prebuilt import create_react_agent
from src.core.state.state import AgentState
import re


class SortingAgent(BaseAgent):
    name = "sorting_tool_agent"
    description = "Understands NL query → returns sorting {column, order} without any tools."

    def __init__(self, llm, auth_token=None):
        # No tools needed
        self.llm = llm
        self.auth_token = auth_token
        self.tools = []

    def build(self):

        prompt = """
You are SortingAgent.

Your ONLY job:
Convert user natural-language sorting instructions into JSON:

{
  "column": "<internal_column>",
  "order": "asc" | "desc"
}

---

### Column Mapping

- "last login", "recent login", "login" → lastlogin
- "last updated", "updated", "modified" → updated
- "name", "person name", "user name" → lastname
- "organization", "primary organization", "org", "company" → organization

---

### Order Mapping

asc  ↦ ascending, low to high, A-Z, oldest first, least, smaller  
desc ↦ descending, high to low, Z-A, newest first, latest, most, bigger  

If no order is given → default "asc"

---

### Rules
- ALWAYS output **only JSON**.
- NEVER add explanation.
- If column is not recognized:
  {
    "error": "Column not found"
  }
- If column is known but order missing → use "asc".

---

### Examples

User: "sort by last login newest first"
→
{
  "column": "lastlogin",
  "order": "desc"
}

User: "order by name"
→
{
  "column": "lastname",
  "order": "asc"
}

User: "sort by organization Z-A"
→
{
  "column": "organization",
  "order": "desc"
}
"""

        agent = create_react_agent(
            model=self.llm,
            tools=[],
            prompt=prompt,
        )

        async def run_with_clear(state: AgentState):
            user_msg = state["prompt"]

            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": user_msg}]}
            )

            messages = result.get("messages", [])
            final_ai_message = None

            # Find final AI message
            for m in reversed(messages):
                role = (
                    getattr(m, "type", None)
                    or m.get("type")
                    or m.__class__.__name__.lower()
                )
                if role in ("ai", "aimessage"):
                    final_ai_message = m
                    break

            # Clean JSON output
            if final_ai_message:
                content = (
                    getattr(final_ai_message, "content", None)
                    or final_ai_message.get("content", "")
                )
                clean = re.sub(
                    r"^```(json|html)?\s*|\s*```$",
                    "",
                    content.strip(),
                    flags=re.MULTILINE,
                )
                final_response = clean.strip()
            else:
                final_response = ""

            structured = {
                "next_agent": "none",
                "final_response": final_response,
                "raw_messages": messages,
            }

            print("✅ SortingAgent Final:", structured)

            state["final_response"] = final_response
            return structured

        return run_with_clear
