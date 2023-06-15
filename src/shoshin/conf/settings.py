import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Shoshin settings"""

    DATABASE_URL: str
    DEFAULT_LANGUAGE: str = "en"
    OPENAI_API_KEY: str
    PROMPT_MAX_TOKENS: int = 2048

    class Config:
        env_file = os.environ.get("SHOSHIN_ENV_FILE", ".env")


settings = Settings()
