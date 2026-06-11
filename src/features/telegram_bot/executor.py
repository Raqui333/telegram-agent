from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from src.features.agent.executor import agent
from src.features.shared.utils import typing
from src.features.shared.logging import logger

from .client import TelegramClient
from .utils import handle_llm_response


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    logger.info(
        f'Message received: chat_id="{message.chat_id}", user_id="{message.from_user.id}" username="{message.from_user.username}"'
    )

    async with typing(context.bot, message.chat_id):
        response = await agent(
            message.text, context.bot, message.chat_id, message.from_user.full_name
        )

        if not response:
            await message.reply_text(
                "Desculpe, eu não consegui processar sua mensagem. 😔"
            )

    await handle_llm_response(message, response)


async def handle_unsupported_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    logger.info(
        f'Audio received: chat_id="{message.chat_id}", user_id="{message.from_user.id}"'
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
