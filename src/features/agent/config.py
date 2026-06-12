from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
    )

    database_url: SecretStr

    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "openai:text-embedding-3-small"

    tavily_api_key: SecretStr

    max_turns_to_trim: int = 10

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        # +psycopg2 is a dependency of sqlalchemy, but we don't need it here
        return value.replace("+psycopg2", "")
