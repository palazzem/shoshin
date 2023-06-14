import os


def test_dotenv_settings(settings):
    # Test settings are overridden by env.testing file
    assert os.environ.get("SHOSHIN_ENV_FILE") == ".env.testing"
    assert settings.DATABASE_URL == "sqlite:///db.testing.sqlite3"
    assert settings.DEFAULT_LANGUAGE == "en"
    assert settings.OPENAI_API_KEY == "sk-000000000000000000000000000000000000000000000000"
    assert settings.PROMPT_MAX_TOKENS == 2048
