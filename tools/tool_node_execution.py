from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode
import json

@tool
def select_correct_table_for_query(keyword: str) -> str:
    """Provides the name of table for a given keyword"""
    table_metadata = {
        "customer": ["CustomerInfo"],
        "user": ["UserInfo"],
        "order": ["OrderInfo"]
    }
    return json.dumps(table_metadata.get(keyword.lower(), "Table not found"))


tools = [select_correct_table_for_query]
tools_by_name = {tool.name: tool for tool in tools}

# Create an AIMessage with tool calls
ai_message = AIMessage(
    content="",
    tool_calls=[
        {
            "name": "select_correct_table_for_query",
            "args": {"keyword": "customer"},
            "id": "call_500560",
            "type": "tool_call",
        }
    ],
)

# Manually execute the tool
print("Executing tool call...")
tool_call = ai_message.tool_calls[0]
tool = tools_by_name[tool_call["name"]]
result = tool.invoke(tool_call["args"])

print(f"Tool: {tool_call['name']}")
print(f"Args: {tool_call['args']}")
print(f"Result: {result}")

# Create tool message
tool_message = ToolMessage(
    content=result,
    tool_call_id=tool_call["id"],
)

print(f"\nTool Message: {tool_message}")
