from typing import TypedDict
import os

from psycopg import connect
from psycopg.rows import dict_row

from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import ToolNode
from langgraph.types import interrupt, Command

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from constants import openai_key, openai_base_url

os.environ["OPENAI_API_KEY"]=openai_key
os.environ["OPENAI_BASE_URL"]=openai_base_url

## OPENNAI LLMS
#getllm = ChatOpenAI(
#    temperature=0.7,
#    model="openai/gpt-5-mini"
#)

getllm = ChatOllama(
    model="llama3.2",
    base_url="http://localhost:11434"
)


DB_CONNECTION_STRING = "postgresql://postgres:<password>@localhost:5432/langgraph_memory"

class CodingAssistantState(TypedDict):
    task: str
    code: str
    tests: str

code_prompt = ChatPromptTemplate.from_template("Geneate Python code for: {task}")
test_prompt = ChatPromptTemplate.from_template("Write unit tests for this code:\n{code}")

code_chain = code_prompt | getllm | StrOutputParser()
test_chain = test_prompt | getllm | StrOutputParser()

def generate_code(state):
    task = state["task"]
    code = code_chain.invoke({"task":task})
    return Command(goto="human_review", update={"code":code})

def human_review(state):
    value = interrupt({
        "question": "Are you ok with the code. Type yes or no : "
    })
    if value == "yes":
        return Command(goto="generate_test")
    else:
        return Command(goto=END)


def generate_test(state):
    task = state["task"]
    code = state["code"]
    tests = test_chain.invoke({"code":code})
    return Command(goto=END, update={"tests":tests})

workflow = StateGraph(CodingAssistantState)
workflow.add_node("generate_code",generate_code)
workflow.add_node("human_review",human_review)
workflow.add_node("generate_test",generate_test)
workflow.set_entry_point("generate_code")

# Create Connection
with connect(DB_CONNECTION_STRING, autocommit=True, prepare_threshold=0, row_factory=dict_row) as conn:

    #checkpointer = MemorySaver()
    checkpointer = PostgresSaver(conn)
    checkpointer.setup()
    graph = workflow.compile(checkpointer=checkpointer)

    thread = {"configurable": {"thread_id":1}}
    response = graph.invoke({"task":"Geneate a code for reversing the string"}, config=thread)
    #print("\n Generated Code -------------")
    #print(response["code"])

    #Each node is stored as task in langgraph state
    tasks = graph.get_state(config=thread).tasks
    print(tasks)
    task = tasks[0]
    question = task.interrupts[0].value.get("question")

    print("\n Question for you  -------------")
    user_input = input(question)
    response = graph.invoke(Command(resume=user_input), config=thread)


    #print(response)
    #print(response.content)
    #print(response["code"])
    #print("/n/n/n")
    #print(response["tests"])

    print(response.get("code","No code generated"))
    print("\n Generated Tests")
    print(response.get("tests","No tests generated"))