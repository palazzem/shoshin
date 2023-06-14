import os

from shoshin.conf import constants as c


def test_dotenv_settings(settings):
    # Test settings are overridden by env.testing file
    assert os.environ.get("SHOSHIN_ENV_FILE") == ".env.testing"
    assert settings.DATABASE_URL == "sqlite:///db.testing.sqlite3"
    assert settings.DEFAULT_LANGUAGE == "en"
    assert settings.OPENAI_API_KEY == "sk-000000000000000000000000000000000000000000000000"
    assert settings.PROMPT_MAX_TOKENS == 2048


def test_constants():
    # Changing these values will break the application
    assert c.EMBEDDING_DIM == 1536
    assert c.EMBEDDING_MODEL == "text-embedding-ada-002"
    assert c.LLM_MODEL == "gpt-3.5-turbo"
    assert c.PREPROCESSOR_SPLIT_LENGTH == 100
    assert c.RETRIEVER_TOP_K == 10
