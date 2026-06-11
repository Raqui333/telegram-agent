from telegram.constants import ParseMode

from langchain.agents.middleware import AgentMiddleware
from src.features.shared.logging import logger


class FeedbackToolCall(AgentMiddleware):
    async def awrap_tool_call(self, request, handler):
        tool_name = request.tool_call["name"]

        ctx: dict = request.runtime.context

        chat_bot = ctx.get("chat_bot", None)
        chat_id = ctx.get("chat_id", None)

        if not chat_bot or not chat_id:
            return await handler(request)

        try:
            await chat_bot.send_message(
                chat_id=chat_id,
                text=f"⚙️ *Using tool*: `{tool_name}`",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        except Exception as e:
            logger.error("Failed to send tool feedback:", repr(e))

        return await handler(request)
