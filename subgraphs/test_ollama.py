from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    base_url="http://localhost:11434"
)

response = llm.invoke("Hello")
print(response.content)