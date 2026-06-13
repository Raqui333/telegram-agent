from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
    )

    database_url: SecretStr

    embedding_model: str = "openai:text-embedding-3-small"

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        # +psycopg2 is a dependency of sqlalchemy, but we don't need it here
        return value.replace("+psycopg2", "")
