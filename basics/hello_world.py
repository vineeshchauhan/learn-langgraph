from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from util.langgraph_util import display 

## State
class HelloWorldState(TypedDict):
    message: str ## it is key

## Hello Node
def hello(state: HelloWorldState):
    print(f"Hello Node: {state['message']}")
    return {"message" : "Hello "+state['message']}


## Bye Node
def bye(state: HelloWorldState):
    print(f"Bye Node: {state['message']}")
    return {"message" : "Bye "+state['message']}


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
outputState = runnable.invoke({"message": "Vineesh"})
print(outputState['message'])
