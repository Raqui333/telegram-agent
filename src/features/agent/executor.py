from dotenv import load_dotenv
from typing import Any
from telegram import Bot

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain_core.messages import HumanMessage

from src.features.shared.logging import logger

from .graph import build_graph
from .config import Settings

load_dotenv()

settings = Settings()

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


async def agent(message: str, chat_bot: Bot, chat_id: int, user_name: str):
    async with AsyncPostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
        await checkpointer.setup()

        agent = build_graph(
            model,
            checkpointer,
        )

        response = await agent.ainvoke(
            {
                "messages": [
                    HumanMessage(content=f"My name is {user_name}\n\n{message}"),
                ]
            },
            config={"configurable": {"thread_id": str(chat_id)}},
            context={"chat_bot": chat_bot, "chat_id": chat_id},
        )

        messages = response.get("messages", [])

        if not messages:
            logger.warning(f'Agent returned no messages: chat_id="{chat_id}"')
            return None

        last_message = messages[-1]
        log_token_usage(last_message, chat_id)

        return last_message.content
