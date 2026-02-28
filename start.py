# start.py

import uuid
from typing import TypedDict, Optional

from langgraph.graph import StateGraph
from langgraph.types import interrupt
from langgraph.checkpoint.postgres import PostgresSaver


class State(TypedDict, total=False):
    approved: bool
    feedback: Optional[str]


def ask_confirmation(state: State):
    # Expect resume payload to be:
    # {"approved": bool, "feedback": Optional[str]}
    payload = interrupt(
        {
            "question": "Approve this operation?",
            "format": {
                "approved": "bool",
                "feedback": "optional string (if not approved)"
            }
        }
    )
    return payload


def final_step(state: State):
    approved = state.get("approved")
    feedback = state.get("feedback")

    print("Operation approved:", approved)

    if approved is False and feedback:
        print("Feedback received:", feedback)

    return {}


builder = StateGraph(State)
builder.add_node("ask", ask_confirmation)
builder.add_node("final", final_step)

builder.set_entry_point("ask")
builder.add_edge("ask", "final")

DB_URL = "postgresql://postgres:postgres@localhost:5432/langgraph"

thread_id = str(uuid.uuid4())

print("\n=== THREAD ID ===")
print(thread_id)
print("=================\n")

with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
    checkpointer.setup()
    graph = builder.compile(checkpointer=checkpointer)

    result = graph.invoke(
        {},
        config={"configurable": {"thread_id": thread_id}},
    )

    print("Paused with interrupt payload:")
    print(result)