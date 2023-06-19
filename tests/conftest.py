import pytest
import responses
from haystack.schema import Document

from shoshin.conf import settings as global_settings


@pytest.fixture
def server():
    """Create a `responses` mock."""
    with responses.RequestsMock() as resp:
        yield resp


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


@pytest.fixture(scope="session")
def audio_file(tmp_path_factory):
    path = tmp_path_factory.mktemp("audio") / "audio.mp3"
    open(path, "w").close()
    yield path


@pytest.fixture(scope="session")
def output_file(tmp_path_factory):
    yield tmp_path_factory.mktemp("output") / "output.bin"


@pytest.fixture(scope="function")
def document():
    content = "This is a test content"
    content_type = "text"
    meta = {"author": "K. Web", "source": "https://example.com"}
    id_hash_keys = ["content"]
    score = None
    embedding = None

    return Document(
        content=content,
        content_type=content_type,
        score=score,
        meta=meta,
        embedding=embedding,
        id_hash_keys=id_hash_keys,
    )
