# resume.py

import sys
from typing import TypedDict, Optional

from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command
from langgraph.checkpoint.postgres import PostgresSaver


if len(sys.argv) < 3:
    print("Usage:")
    print("  python resume.py <thread_id> true")
    print("  python resume.py <thread_id> false \"feedback text\"")
    sys.exit(1)

thread_id = sys.argv[1]
approved_input = sys.argv[2].lower()

if approved_input not in ("true", "false"):
    print("Second argument must be 'true' or 'false'")
    sys.exit(1)

approved = approved_input == "true"

feedback = None
if not approved:
    if len(sys.argv) >= 4:
        feedback = sys.argv[3]
    else:
        feedback = ""


class State(TypedDict, total=False):
    approved: bool
    feedback: Optional[str]


def ask_confirmation(state: State):
    payload = interrupt(
        {
            "question": "Approve this operation?",
            "format": {
                "approved": "bool",
                "feedback": "optional string"
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

with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)

    graph.invoke(
        Command(resume={"approved": approved, "feedback": feedback}),
        config={"configurable": {"thread_id": thread_id}},
    )