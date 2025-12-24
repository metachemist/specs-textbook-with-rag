import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Physical AI & Humanoid Robotics Textbook API"

    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    NEON_DATABASE_URL: str = os.getenv("NEON_DATABASE_URL", "")

    # Qdrant Settings
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Cohere Settings
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # Better Auth Settings
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-here")
    BETTER_AUTH_URL: str = os.getenv("BETTER_AUTH_URL", "http://localhost:8000/auth")

    # Frontend URL
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Deployment settings
    DEPLOYED_VERCEL_URL: str = os.getenv("DEPLOYED_VERCEL_URL", "")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()