from telegram.ext import ApplicationBuilder
from .config import Settings


class TelegramClient:
    def __init__(self):
        settings = Settings()
        if not settings.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN was not provided")

        TOKEN = settings.telegram_bot_token.get_secret_value()
        self.bot = ApplicationBuilder().token(TOKEN).build()

    def start(self):
        self.bot.run_polling()
