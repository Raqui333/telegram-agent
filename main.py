from telegram.ext import Application, ApplicationBuilder

from src.features.telegram_bot.config import Settings
from src.features.telegram_bot.handlers import register_handlers

from src.services.langgraph_persistence.client import langgraph_persistence_client

async def post_init(app: Application) -> None:
    await langgraph_persistence_client.start()

async def post_shutdown(app: Application) -> None:
    await langgraph_persistence_client.stop()

def main() -> None:
    settings = Settings()
    token = settings.telegram_bot_token.get_secret_value()

    app = (
        ApplicationBuilder()
        .token(token)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )

    register_handlers(app)

    app.run_polling()

if __name__ == "__main__":
    main()