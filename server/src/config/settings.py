import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # API Keys
    cohere_api_key: str = Field(default=..., description="Cohere API Key")
    qdrant_api_key: str = Field(default=..., description="Qdrant API Key")
    qdrant_url: str = Field(default=..., description="Qdrant Cloud URL")

    # Application settings
    log_level: str = Field(default="INFO", description="Logging level")
    chunk_size: int = Field(default=800, description="Target size for text chunks in tokens")
    overlap: int = Field(default=100, description="Overlap between chunks in tokens")
    max_concurrent_fetches: int = Field(default=5, description="Maximum concurrent URL fetches")
    request_timeout: int = Field(default=30, description="Request timeout in seconds")

    # Qdrant settings
    qdrant_collection_name: str = Field(default="web_content_embeddings", description="Qdrant collection name")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a singleton instance of settings
settings = Settings()