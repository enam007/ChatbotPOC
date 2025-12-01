
from src.core.mcp.tools.filter_tools.registry import FILTER_TOOLS


TOOL_NAMESPACES = {
   
    "filter_tool_agent": FILTER_TOOLS,
}


def get_tools_for(agent_name: str):
    """Return tools registered for the given agent as a name:function dict."""
    return TOOL_NAMESPACES.get(agent_name, [])