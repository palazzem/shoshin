import pytest
import responses
from haystack.schema import Document
from milvus_documentstore import MilvusDocumentStore

from shoshin.conf import constants
from shoshin.conf import settings as global_settings
from shoshin.datastore.documents import DocumentStore


@pytest.fixture
def server():
    """Create a `responses` mock."""
    with responses.RequestsMock() as resp:
        yield resp


@pytest.fixture(scope="function", autouse=True)
def tenacity(mocker):
    """Mock tenacity to skip retries for mocked tests."""
    mocker.patch("tenacity.nap.time.sleep")


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
def vector():
    """
    Provides a JSON string containing test embeddings vectors for use in test cases.

    These embeddings vectors are simulated outputs from the 'text-embedding-ada-002' model by OpenAI.
    This fixture acts as a mock for the actual response expected from the OpenAI API.

    This fixture can be paired with the `responses` library in test cases to simulate API calls
    and responses, thereby enabling isolated testing of code that interacts with the OpenAI API.

    Yields:
        str: A JSON string containing embeddings vectors, read from a local fixture file.
    """
    with open("tests/fixtures/embeddings_vectors.json") as f:
        response = f.read()
    yield response


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


@pytest.fixture(scope="function")
def milvus(settings):
    ds = MilvusDocumentStore(
        embedding_dim=constants.EMBEDDING_DIM, sql_url=settings.DATABASE_URL, progress_bar=settings.PROGRESS_BAR
    )
    ds.delete_all_documents()
    yield ds
    ds.delete_all_documents()


@pytest.fixture(scope="function")
def document_store(mocker):
    mocker.patch("shoshin.datastore.documents.MilvusDocumentStore")
    mocker.patch("shoshin.datastore.documents.EmbeddingRetriever")
    yield DocumentStore()
