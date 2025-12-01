# src/agents/filter_agent.py

from src.core.agents.base_agent import BaseAgent
from src.core.mcp.tools.tool_registry import get_tools_for
from functools import partial
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import StructuredTool
from pydantic import create_model
from src.core.state.state import AgentState
from langchain_core.prompts import ChatPromptTemplate
import re


class FilterAgent(BaseAgent):
    name = "filter_tool_agent"
    description = "Understands NL query → resolves filter → returns {column, value_id}. Uses tools to map names→IDs."

    def __init__(self, llm, auth_token):
        base_tools = get_tools_for(self.name)
        self.llm = llm
        self.auth_token = auth_token
        self.tools = []

        print("🔧 Loaded Base Tools:", base_tools)

        # ✅ auto-inject token param to tools that require it
        for tool in base_tools:
            func = getattr(tool, "func", None) or getattr(tool, "coroutine", None)
            if not callable(func):
                continue

            if "token" in tool.args:
                wrapped = partial(func, token=self.auth_token)
                orig_schema = tool.args_schema

                if orig_schema and hasattr(orig_schema, "__fields__"):
                    new_fields = {
                        k: v
                        for k, v in orig_schema.__fields__.items()
                        if k != "token"
                    }

                    NewSchema = create_model(
                        f"{orig_schema.__name__}NoToken",
                        **{
                            f_name: (fld.outer_type_, fld.default)
                            for f_name, fld in new_fields.items()
                        },
                    )

                    new_tool = tool.copy(
                        update={
                            "coroutine": wrapped,
                            "args_schema": NewSchema,
                        }
                    )
                else:
                    new_tool = tool.copy(
                        update={"coroutine": wrapped}
                    )
            else:
                new_tool = tool

            self.tools.append(new_tool)

    def build(self):
        # ✅ SYSTEM PROMPT
        prompt = """
       You are Filter_Tool_Agent.

🎯 Goal
- Convert a natural-language user request into a structured filter.
- Identify which column the user wants to filter.
- Identify which tool can resolve the value to an ID.
- Use the tool to get the value ID.
- Output a valid normalized JSON response.

✅ OUTPUT FORMAT
Always respond with JSON only:
{
  "column": "<column_name>",
  "value_id": "<id>"
}

🚨 RULES
- NEVER return raw text. Always resolve the value via the correct tool.
- Infer column from context (examples):
  - "ACCG" → organization
  - "John Doe" → person
  - "Miami" → city
- Determine which tool is appropriate for the column.
- If ambiguous → ask a clarifying question.
- If value not found, respond with:
{
  "error": "Value not found"
}

✅ RESPONSIBILITIES
1. Infer column from user input.
2. Select the correct tool for that column.
3. Call the tool to resolve the value to an ID.
4. Return only the final JSON.

✅ EXAMPLE
User: "show me all people from organization ACCG"
- Determine "ACCG" refers to "organization"
- Call GetOrganizationListWithIdForFilters
- Return:
{
  "column": "organization",
  "value_id": "12345"
}
        """

        agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=prompt,
            
        )

        async def run_with_clear(state: AgentState):
            user_msg = state["prompt"]              # user message from state

            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": user_msg}]}
            )

            #result = await agent.ainvoke(state)

            messages = result.get("messages", [])
            final_ai_message = None

            for m in reversed(messages):
                role = getattr(m, "type", None) or m.get("type") or m.__class__.__name__.lower()
                if role in ("ai", "aimessage"):
                    final_ai_message = m
                    break

            if final_ai_message:
                content = (
                    getattr(final_ai_message, "content", None)
                    or final_ai_message.get("content", "")
                )
                clean = re.sub(r"^```(json|html)?\s*|\s*```$", "", content.strip(), flags=re.MULTILINE)
                final_response = clean.strip()
            else:
                final_response = ""

            structured = {
                "next_agent": "none",
                "final_response": final_response,
                "raw_messages": messages,
            }

            print("✅ FilterAgent Final:", structured)

            #state["next_agent"] = "none"
            state["final_response"] = final_response
            return structured

        return run_with_clear
