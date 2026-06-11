from langchain.agents.middleware import before_agent, AgentState
from langchain_core.messages import HumanMessage, RemoveMessage
from langgraph.runtime import Runtime

from ..config import Settings

settings = Settings()

MAX_TURNS_TO_TRIM = settings.max_turns_to_trim


@before_agent
def trim_messages(state: AgentState, runtime: Runtime):
    messages = state["messages"]

    # Find the indices where each turn starts (each HumanMessage)
    boundaries = [i for i, m in enumerate(messages) if isinstance(m, HumanMessage)]

    # If we have few turns, no need to trim
    if len(boundaries) <= MAX_TURNS_TO_TRIM:
        return None

    # The cutoff is the start of the Nth turn counting from the back
    cutoff = boundaries[-MAX_TURNS_TO_TRIM]

    # Remove everything before the cutoff
    messages_to_remove = messages[:cutoff]

    return {
        "messages": [
            RemoveMessage(id=m.id) for m in messages_to_remove if m.id is not None
        ]
    }
