## Search Tools
## Retrieval Tools
## Calculation Tools
## Code Execution Tools
## Data Querying Tools
## File Manipulation Tools
## Custom API Tools

import os
from constants import openai_key
from constants import openai_base_url
from langchain_openai import ChatOpenAI
from typing import TypedDict
from langchain_core.tools import tool
from langgraph.graph import END, START
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import json
import base64

class StateMessage(TypedDict):
    messages: str

os.environ["OPENAI_API_KEY"]=openai_key
os.environ["OPENAI_BASE_URL"]=openai_base_url

## OPENNAI LLMS
getllm = ChatOpenAI(
    temperature=0.7,
    model="openai/gpt-5-mini"
)

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
llm = getllm.bind_tools(tools)
messages = [
    HumanMessage("Can you fetch information about the user with id 123?")
]

response = llm.invoke(messages)
print("\nRespone:", response)

# Check if the LLM wants to call a tool
if hasattr(response, 'tool_calls') and response.tool_calls:
    print("\nTool calls detected:")
    for tool_call in response.tool_calls:
        print(f"  - Tool: {tool_call['name']}")
        print(f"    Args: {tool_call['args']}")
else:
    print("\nNo tool calls detected")


tool_node = ToolNode(tools)
message_with_tool_call = AIMessage(content="", tool_calls=[{'name': 'select_correct_table_for_query', 
                                                            'args': {'keyword': 'user'}, 
                                                            'id': 'call_uFlK3A5vTFkk1TfubDZWlVzf', 
                                                            'type': 'tool_call'}])

from langgraph.runtime import Runtime
runtime = Runtime()
config = {"configurable": {"__pregel_runtime": runtime}}
resp1 = tool_node.invoke({"messages": [message_with_tool_call]}, config=config)

print(resp1)