import logging
import uuid

from langchain.tools import tool, ToolRuntime
from telegram.constants import ParseMode

from ..schemas import Context

logger = logging.getLogger(__name__)


@tool
async def save_memory(memory: str, runtime: ToolRuntime[Context]):
    """
    Save a memory.

    Only save information that is likely to be useful in future conversations, such as:
    - preferences
    - goals
    - background
    - recurring habits
    - important decisions
    - personal context

    The memory must be written as a single concise, self-contained sentence that can be understood without additional context.
    """

    logger.info(f'Tool called: name="save_memory" memory="{memory}"')

    try:
        # Get the chat id from the runtime context
        chat_id = runtime.context["chat_id"]

        namespace = (str(chat_id), "memories")
        memory_id = str(uuid.uuid4())

        # Create a new memory
        await runtime.store.aput(namespace, memory_id, {"memory": memory})

        # get telegram bot client from the runtime context for feedback
        bot_client = runtime.context["telegram_bot_client"]

        await bot_client.send_message(
            chat_id=chat_id,
            text=f"🧠 `{memory}`",
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        return "Memória salva com sucesso."
    except Exception as exc:
        logger.error(f"Error saving memory: {exc}")
        return "Falha ao salvar memória no momento."


@tool
async def read_memory(query: str, runtime: ToolRuntime[Context]):
    """
    Read a memory.

    Use this tool when user-specific context may help answer the request, including:

    - preferences
    - goals
    - background
    - ongoing projects
    - previous decisions
    - constraints

    Search using the most relevant keywords from the current conversation and return only memories that are useful for the current task.
    """

    logger.info(f'Tool called: name="read_memory" query="{query}"')

    try:
        chat_id = runtime.context["chat_id"]
        store = runtime.store

        if not store:
            return "Nenhuma memória encontrada."

        namespace = (str(chat_id), "memories")

        # Search for memories
        results = await store.asearch(namespace, query=query, limit=10)

        if not results:
            return "Nenhuma memória relevante encontrada."

        memories: list[str] = []

        for item in results:
            value = item.value if hasattr(item, "value") else item

            if isinstance(value, dict):
                text = str(value.get("memory", value))
            else:
                text = str(value)

            text = text.strip()

            if text:
                memories.append(text)

        if not memories:
            return "Nenhuma memória relevante encontrada."

        lines = ["Memórias relevantes encontradas:"]
        lines.extend(f"- {text}" for text in memories)

        return "\n".join(lines)
    except Exception as exc:
        logger.error(f"Error reading memory: {exc}")
        return "Falha ao buscar memórias no momento."
