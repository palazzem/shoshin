import os

from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Shoshin settings"""

    DATABASE_URL: str
    DEFAULT_LANGUAGE: str = "en"
    OPENAI_API_KEY: str
    PROMPT_MAX_TOKENS: int = 2048

    class Config:
        env_file = os.environ.get("SHOSHIN_ENV_FILE", ".env")


# Load environment variables and initialize settings
load_dotenv(Settings.Config.env_file, override=True)
settings = Settings()
