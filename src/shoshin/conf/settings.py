from dotenv import dotenv_values
from pysettings.base import BaseSettings
from pysettings.options import Option


class Settings(BaseSettings):
    """Shoshin settings"""

    DATABASE_URL = Option(default="sqlite:///db.sqlite3", not_null=True)
    DEFAULT_LANGUAGE = Option(default="en", not_null=True)
    OPENAI_API_KEY = Option(not_null=True)
    PROMPT_MAX_TOKENS = Option(default=2048, not_null=True)


# Take environment variables from `.env` file
env_config = dotenv_values(".env")

# Update settings with environment variables
settings = Settings()
for attr, value in env_config.items():
    settings[attr] = value

# Validate settings
settings.is_valid()
