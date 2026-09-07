from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class SupportRequest(TypedDict):
    message : str
    priority : int

def categorize_request(request: SupportRequest):
    if "urgent" in request['message'].lower() or request['priority'] == 1:
        return "high"
    return "low"


def handle_urgent(request: SupportRequest):
    print(f"Received Urgent Request : {request["message"]}")
    return request


def handle_standard(request: SupportRequest):
    print(f"Received Standard Request : {request["message"]}")
    return request


graph = StateGraph(SupportRequest)

graph.add_node("urgent",handle_urgent)
graph.add_node("standard",handle_standard)

graph.add_conditional_edges(START, categorize_request,{"high":"urgent","low":"standard"})
graph.add_edge("urgent",END)
graph.add_edge("standard",END)

runnable = graph.compile()

output = runnable.invoke({"message" : "urgent request","priority" : 1})
output = runnable.invoke({"message" : "standard request","priority" : 2})

print(output)
