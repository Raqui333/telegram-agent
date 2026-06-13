import logging

from dotenv import load_dotenv
from typing import Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from src.services.langgraph_persistence.client import langgraph_persistence_client

from .graph import build_graph
from .schemas import Context
from .config import Settings

logger = logging.getLogger(__name__)
settings = Settings()

load_dotenv()

DATABASE_URL = settings.database_url.get_secret_value()

model = ChatOpenAI(
    model=settings.openai_model,
    temperature=0.7,
)


def log_token_usage(last_message: dict[str, Any], chat_id: int):
    usage_metadata: dict[str, int] = getattr(last_message, "usage_metadata", None)

    if not usage_metadata:
        return

    input_tokens = usage_metadata.get("input_tokens", 0)
    output_tokens = usage_metadata.get("output_tokens", 0)
    total_tokens = usage_metadata.get("total_tokens", 0)

    logger.info(
        f'Agent response: chat_id="{chat_id}" input_tokens="{input_tokens}" output_tokens="{output_tokens}" total_tokens="{total_tokens}"'
    )


async def agent(context: Context, text: str):
    try:
        checkpointer, store = langgraph_persistence_client.get_instance()

        agent = build_graph(
            model,
            checkpointer,
            store,
        )

        llm_input = {
            "messages": [
                HumanMessage(content=f"My name is {context["user_name"]}\n\n{text}"),
            ]
        }

        response = await agent.ainvoke(
            input=llm_input,
            context=context,
            config={"configurable": {"thread_id": str(context["chat_id"])}},
        )

        messages = response.get("messages", [])

        if not messages:
            logger.warning(
                f'Agent returned no messages: chat_id="{context["chat_id"]}"'
            )
            return None

        last_message = messages[-1]
        log_token_usage(last_message, context["chat_id"])

        return last_message.content
    except Exception as e:
        logger.error(f"Error in agent: {e}")
        return "Não consegui processar sua mensagem. 😔"
