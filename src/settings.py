from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    LOG_LEVEL: str = "info"
    DATABASE_URL: str = ""

    # OIDC Configuration
    OIDC_CLIENT_ID: str = ""
    OIDC_CLIENT_SECRET: str = ""
    OIDC_ISSUER_URL: str = ""
    OIDC_VERIFY_SSL: bool = True

    # Session
    SESSION_SECRET_KEY: str = "change-me-to-a-random-secret"

    # Casbin
    CASBIN_MODEL_PATH: str = str(Path(__file__).parent / "config" / "casbin_model.conf")
    CASBIN_POLICY_PATH: str = str(Path(__file__).parent / "config" / "casbin_policy.conf")

    # RAG/Vector Search Configuration
    EMBEDDINGS_ENABLED: bool = False
    COHERE_API_KEY: str = ""
    EMBEDDING_MODEL: str = "embed-english-v3.0"
    EMBEDDING_DIMENSION: int = 1536
    SIMILARITY_THRESHOLD: float = 0.5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = ServerSettings()
