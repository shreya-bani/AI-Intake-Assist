from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables."""

    # LLM Provider Configuration
    LLM_PROVIDER: str = "openai"
    MODEL_NAME: str = "gpt-4-turbo-preview"

    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # Application Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    SESSION_TIMEOUT_MINUTES: int = 30

    # CORS Settings
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    def validate_llm_config(self) -> None:
        """Validate that the required API key is present for the selected provider."""
        if self.LLM_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set when LLM_PROVIDER is 'openai'")
        elif self.LLM_PROVIDER == "anthropic" and not self.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY must be set when LLM_PROVIDER is 'anthropic'")
        elif self.LLM_PROVIDER not in ["openai", "anthropic"]:
            raise ValueError(f"Invalid LLM_PROVIDER: {self.LLM_PROVIDER}. Must be 'openai' or 'anthropic'")


# Create a global settings instance
settings = Settings()

# Validate configuration on load
try:
    settings.validate_llm_config()
except ValueError as e:
    if not settings.DEBUG:
        raise
    print(f"Warning: {e}")
