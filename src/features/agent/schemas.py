from typing_extensions import TypedDict
from telegram import Bot

class Context(TypedDict):
    user_name: str
    chat_id: int
    telegram_bot_client: Bot
