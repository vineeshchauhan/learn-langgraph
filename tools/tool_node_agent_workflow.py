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
from langgraph.graph import StateGraph, END, START, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import json

##class StateMessage(TypedDict):
##    messages: str

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
tool_node = ToolNode(tools)


def call_model(state: MessagesState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages" : response}

def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(MessagesState)

workflow.add_node("agent",call_model)
workflow.add_node("tools",tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent",should_continue)
## The tool node should execute the tool call and return response to agent to that
## the agent can format the response and perform next function.
workflow.add_edge("tools", "agent") 

messages = [
    HumanMessage(content="Can you fetch information about the user with id 123? Only return the name of the table and tool used in the output")
]

response = workflow.compile().invoke({"messages": messages})
print("\nRespone:", response)
