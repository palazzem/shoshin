import os

from pysettings.base import BaseSettings
from pysettings.options import Option


class Settings(BaseSettings):
    """Shoshin settings"""

    DATABASE_URL = Option(default="sqlite:///db.sqlite3", not_null=True)
    DEFAULT_LANGUAGE = Option(default="en", not_null=True)
    OPENAI_API_KEY = Option(not_null=True)
    PROMPT_MAX_TOKENS = Option(default=2048, not_null=True)


# Get values from environment variables
settings = Settings()
settings.DATABASE_URL = os.getenv("SHOSHIN_DATABASE_URL", settings.DATABASE_URL)
settings.DEFAULT_LANGUAGE = os.getenv("SHOSHIN_DEFAULT_LANGUAGE", settings.DEFAULT_LANGUAGE)
settings.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
settings.PROMPT_MAX_TOKENS = os.getenv("SHOSHIN_PROMPT_MAX_TOKENS", settings.PROMPT_MAX_TOKENS)
settings.is_valid()
