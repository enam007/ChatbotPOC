from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.core.state.state import AgentState,IntentOutput


class IntentParserNode:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm.with_structured_output(IntentOutput)

    async def __call__(self, state: AgentState):
        user_prompt = state["prompt"]

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an intent classification assistant. 
Analyze the user's message and determine if they want to:
- FILTER: Apply a filter to data based on column and value
- SORT: Sort data by a column in ascending or descending order
- UNKNOWN: Neither filtering nor sorting"""),
            ("user", "{prompt}")
        ])

        formatted_prompt = prompt_template.format(prompt=user_prompt)
        title: IntentOutput = await self.llm.ainvoke(formatted_prompt)

        state["intent"] = title.intent  # assuming IntentOutput has .intent
        return state
