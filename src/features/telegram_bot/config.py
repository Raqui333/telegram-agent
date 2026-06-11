from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from telegramify_markdown.config import get_runtime_config

cfg = get_runtime_config()
cfg.markdown_symbol.heading_level_1 = ""
cfg.markdown_symbol.heading_level_2 = ""
cfg.markdown_symbol.heading_level_3 = ""
cfg.markdown_symbol.heading_level_4 = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
    )

    telegram_bot_token: SecretStr
