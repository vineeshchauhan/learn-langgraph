from pydantic import BaseModel, Field
from langgraph.graph import END, START, StateGraph
from util.langgraph_util import display 
from pydantic import BaseModel
from typing import Optional

## State
class HelloWorldState(BaseModel):
    message: str = Field(min_length=3,max_length=100)
    id: Optional[int] = None

## Hello Node
def hello(state: HelloWorldState):
    print(f"Hello Node: {state.message}")
    return {"message" : "Hello "+state.message}


## Bye Node
def bye(state: HelloWorldState):
    print(f"Bye Node: {state.message}")
    return {"message" : "Bye "+state.message}


## Create a graph
graph = StateGraph(HelloWorldState)

##add nodes
graph.add_node("hello",hello)
graph.add_node("bye",bye)

## add edges
#graph.add_edge(START, "hello")
##
graph.set_entry_point("hello")

graph.add_edge("hello", "bye")
graph.add_edge("bye", END)

## compile the graph
runnable = graph.compile()
#display(runnable)

## run the graph
outputState = runnable.invoke({"message": "Vineesh","id":123})
print(outputState['message'])
