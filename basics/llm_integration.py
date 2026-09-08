from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import json
import base64

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
            temperature=0.9,
            max_output_tokens=4096,
        )


messages = [
    SystemMessage(content="You are a helpful AI assistant."),
    HumanMessage(content="Who is Bibhu Tripathy at UKG?")
]

llm = get_llm()

response = llm.invoke(messages)

print(response.content)
