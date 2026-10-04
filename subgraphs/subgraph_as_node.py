from typing import TypedDict
import os
from langgraph.graph import END, START, StateGraph
from constants import openai_key, openai_base_url

class InsuranceState(TypedDict):
    patient_id: int
    insurance_verified: bool

def verify_insurance_check(state: InsuranceState):
    print("verify_insurance_check")
    if state["patient_id"] is not None:
        return {"insurance_verified": True, "appointment_status":"Insurance verification is in progress"}
    else:
        return {"insurance_verified": False, "appointment_status":"Insurance verification is in pending"}
        

def verify_insurance_confirm(state: InsuranceState):
    print("verify_insurance_confirm")
    if state["insurance_verified"]:
        return {"appointment_status":"Insurance verified"}
    else:
        return {"appointment_status":"Insurance verification failed"}

workflow = StateGraph(InsuranceState)
workflow.add_node("verify_insurance_check" , verify_insurance_check)
workflow.add_node("verify_insurance_confirm" , verify_insurance_confirm)

workflow.add_edge(START,"verify_insurance_check")
workflow.add_edge("verify_insurance_check","verify_insurance_confirm")
workflow.add_edge("verify_insurance_confirm",END)

insurance_verification_graph = workflow.compile()


# Define Shared State
class AppointmentState(TypedDict):
    patient_id: int
    appointment_status: str
    insurance_verified: bool
    appointment_scheduled: bool


def schedule_appointment(state: AppointmentState):
    print("schedule_appointnment")
    if state["insurance_verified"]:
        return {"appointment_scheduled": True, "appointment_status":"Appointment Scheduled"}
    else:
        return {"appointment_scheduled": False, "appointment_status":"Appointment Scheduling failed"}


appointment_workflow = StateGraph(AppointmentState)
appointment_workflow.add_node("schedule_appointment" , schedule_appointment)
appointment_workflow.add_node("insurance_verification" , insurance_verification_graph)

appointment_workflow.add_edge(START,"insurance_verification")
appointment_workflow.add_edge("insurance_verification","schedule_appointment")
appointment_workflow.add_edge("schedule_appointment",END)

graph = appointment_workflow.compile()

inputs = {
    "patient_id" : None
}

output = graph.invoke(inputs)

print(output)