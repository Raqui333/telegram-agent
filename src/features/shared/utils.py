import asyncio

from contextlib import asynccontextmanager, suppress

from telegram import Bot
from telegram.constants import ChatAction


async def typing_loop(chat_bot: Bot, chat_id: int):
    while True:
        try:
            await chat_bot.send_chat_action(
                chat_id=chat_id,
                action=ChatAction.TYPING,
            )
        except Exception:
            return

        await asyncio.sleep(4)


@asynccontextmanager
async def typing(chat_bot: Bot, chat_id: int):
    """
    Context manager to send a typing action to the chat.
    It will send a typing action every 4 seconds until the context is exited.
    This is used to keep the user informed that the bot is thinking.
    """
    task = asyncio.create_task(typing_loop(chat_bot, chat_id))

    try:
        yield
    finally:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
