import pytest

from shoshin.conf import settings as global_settings


@pytest.fixture(scope="function")
def settings():
    """
    Fixture that creates a copy of the current configuration settings before each test function,
    and restores the original settings after the test has completed. This ensures that any changes made
    to the configuration during the test do not affect other tests.

    Returns:
        The current Shoshin configuration settings.
    """
    previous_settings = global_settings.dict()
    yield global_settings
    global_settings.__dict__.update(previous_settings)


@pytest.fixture(scope="function")
def ffmpeg(mocker):
    """
    Fixture that mocks the `ffmpeg` module for testing purposes.

    Returns:
        The mocked `ffmpeg` module.
    """
    return mocker.patch("shoshin.pipeline.processors.ffmpeg")
