"""Core configuration management."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Multi-Agent RAG System"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = Field(default="development", alias="ENV")

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/rag_system",
        alias="DATABASE_URL",
    )

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    # OpenSearch
    opensearch_host: str = Field(default="localhost", alias="OPENSEARCH_HOST")
    opensearch_port: int = Field(default=9200, alias="OPENSEARCH_PORT")
    opensearch_use_ssl: bool = Field(default=False, alias="OPENSEARCH_USE_SSL")

    # Authentication
    secret_key: str = Field(
        default="your-secret-key-change-in-production", alias="SECRET_KEY"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # LLM Configuration
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_URL")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    # Langfuse
    langfuse_secret_key: str | None = Field(default=None, alias="LANGFUSE_SECRET_KEY")
    langfuse_public_key: str | None = Field(default=None, alias="LANGFUSE_PUBLIC_KEY")
    langfuse_host: str = Field(
        default="https://cloud.langfuse.com", alias="LANGFUSE_HOST"
    )

    # File Storage
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # CORS
    cors_origins: list[str] = ["*"]

    # Agent settings
    max_concurrent_agents: int = 5
    agent_timeout_seconds: int = 300

    # Embedding settings
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    # arXiv settings
    arxiv_base_url: str = "http://export.arxiv.org/api/query"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
