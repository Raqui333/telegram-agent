from langchain.agents import create_agent
from langgraph.checkpoint.base import BaseCheckpointSaver
from langchain_core.language_models import BaseChatModel

from .prompts.system_prompt import SYSTEM_PROMPT
from .schemas import ContextSchema

# tools
from .tools.web_search import web_search
from .tools.get_current_datetime import get_current_datetime

# middlewares
from .middlewares.trim_messages import trim_messages
from .middlewares.feedback_tool_call import FeedbackToolCall


def build_graph(
    model: BaseChatModel,
    checkpointer: BaseCheckpointSaver | None = None,
):
    return create_agent(
        model=model,
        tools=[get_current_datetime, web_search],
        system_prompt=SYSTEM_PROMPT,
        middleware=[trim_messages, FeedbackToolCall()],
        context_schema=ContextSchema,
        checkpointer=checkpointer,
    )
