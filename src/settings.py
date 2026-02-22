from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    LOG_LEVEL: str = "info"
    DATABASE_URL: PostgresDsn

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = ServerSettings()  # ty:ignore[missing-argument]
