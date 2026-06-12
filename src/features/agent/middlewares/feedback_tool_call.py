from telegram.constants import ParseMode

from langchain.agents.middleware import AgentMiddleware
from src.features.shared.logging import logger


class FeedbackToolCall(AgentMiddleware):
    async def awrap_tool_call(self, request, handler):
        tool_name = request.tool_call["name"]

        ctx: dict = request.runtime.context

        chat_id = ctx.get("chat_id", None)
        telegram_bot_client = ctx.get("telegram_bot_client", None)

        if not telegram_bot_client or not chat_id:
            return await handler(request)

        try:
            await telegram_bot_client.send_message(
                chat_id=chat_id,
                text=f"⚙️ *Using tool*: `{tool_name}`",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        except Exception as e:
            logger.error("Failed to send tool feedback:", repr(e))

        return await handler(request)
