import os

from dotenv import dotenv_values
from pysettings.base import BaseSettings
from pysettings.options import Option


class Settings(BaseSettings):
    """Shoshin settings"""

    DATABASE_URL = Option(default="sqlite:///db.sqlite3", allow_null=False)
    DEFAULT_LANGUAGE = Option(default="en", allow_null=False)
    OPENAI_API_KEY = Option(allow_null=False)
    PROMPT_MAX_TOKENS = Option(default=2048, allow_null=False)


# Take environment variables from `.env` file
env_file = os.environ.get("SHOSHIN_ENV_FILE", ".env")
env_config = dotenv_values(env_file)

# Update settings with environment variables
settings = Settings()
for attr, value in env_config.items():
    setattr(settings, attr, value)

# Validate settings
settings.is_valid()
