import os
from constants import openai_key
from constants import openai_base_url
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.types import interrupt
from langgraph.types import Command

os.environ["OPENAI_API_KEY"]=openai_key
os.environ["OPENAI_BASE_URL"]=openai_base_url

## OPENNAI LLMS
getllm = ChatOpenAI(
    temperature=0.7,
    model="openai/gpt-5-mini"
)

class CodingAssistantState(TypedDict):
    task: str
    code: str
    tests: str

code_prompt = ChatPromptTemplate.from_template("Geneate Python code for: {task}")
test_prompt = ChatPromptTemplate.from_template("Write unit tests for this code:\n{code}")

code_chain = code_prompt | getllm | StrOutputParser()
test_chain = test_prompt | getllm | StrOutputParser()

def geneate_code(state):
    task = state["task"]
    code = code_chain.invoke({"task":task})
    return {"task":task, "code":code}

def geneate_test(state):
    task = state["task"]
    code = state["code"]
    tests = test_chain.invoke({"code":code})
    return {"task":task, "code":code,"tests":tests}

workflow = StateGraph(CodingAssistantState)
workflow.add_node("geneate_code",geneate_code)
workflow.add_node("geneate_test",geneate_test)

workflow.add_edge(START, "geneate_code")
workflow.add_edge("geneate_code", "geneate_test")
workflow.add_edge("geneate_test", END)

graph = workflow.compile()

response = graph.invoke({"task":"Geneate a code for reversing the string"})
print(response)
#print(response.content)
print(response["code"])
print("/n/n/n")
print(response["tests"])