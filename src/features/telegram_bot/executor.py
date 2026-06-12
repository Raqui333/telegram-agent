import logging

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from src.features.agent.executor import agent
from src.features.shared.utils import typing
from src.features.agent.schemas import Context

from .client import TelegramClient
from .utils import handle_llm_response

logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    logger.info(
        f'Message received: chat_id="{message.chat_id}", user_id="{message.from_user.id}"'
    )

    async with typing(context.bot, message.chat_id):
        context = Context(
            chat_id=message.chat_id,
            user_name=message.from_user.full_name,
            telegram_bot_client=context.bot,
        )

        try:
            response = await agent(context, message.text)

            if not response:
                raise Exception("Agent returned no response")

            await handle_llm_response(message, response)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

            await message.reply_text(
                "Desculpe, eu não consegui processar sua mensagem. 😔"
            )


async def handle_unsupported_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    logger.info(
        f'Unsupported media received: chat_id="{message.chat_id}", user_id="{message.from_user.id}"'
    )

    await message.reply_text("Desculpe, eu não suporto esse tipo de mídia ainda. 😔")


def executor():
    client = TelegramClient()

    client.bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    client.bot.add_handler(
        MessageHandler(~filters.TEXT & ~filters.COMMAND, handle_unsupported_media)
    )

    client.start()


if __name__ == "__main__":
    executor()
