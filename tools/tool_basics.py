from typing import TypedDict
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage
from langgraph.prebuild import ToolNode
import json
import base64

class StateMessage(TypedDict):
    messages: str

GCP_SERVICE_ACCOUNT_VERTEX_AI=""
VERTEX_AI_LOCATION="global"
VERTEX_AI_MODEL="gemini-3.8-flash"
VERTEX_AI_MAX_TOKENS=4096
VERTEX_AI_TEMPERATURE=0.7

def get_llm() -> ChatGoogleGenerativeAI:
    if GCP_SERVICE_ACCOUNT_VERTEX_AI:
        from google.oauth2 import service_account

        # Decode base64 if needed, otherwise treat as raw JSON — both formats are accepted.
        try:
            json.loads(GCP_SERVICE_ACCOUNT_VERTEX_AI)
            credentials_str = GCP_SERVICE_ACCOUNT_VERTEX_AI
        except json.JSONDecodeError:
            credentials_str = base64.b64decode(GCP_SERVICE_ACCOUNT_VERTEX_AI).decode("utf-8")

        credentials_info = json.loads(credentials_str)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        return ChatGoogleGenerativeAI(
            model=VERTEX_AI_MODEL,
            project=credentials_info["project_id"],
            location=VERTEX_AI_LOCATION,
            credentials=credentials,
            temperature=0.7,
            max_output_tokens=4096,
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
llm = get_llm().bind_tools(tools)
messages = [
    HumanMessage("Can you fetch information about the customer with id 123?")
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
