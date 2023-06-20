import pytest
import responses
from haystack.errors import OpenAIError

from shoshin.exceptions import AIError
from shoshin.pipeline import embeddings


def test_embeddings_create(milvus, document, server, vector):
    # Ensure embeddings.create stores the embedding in the document store.
    server.add(
        responses.POST,
        "https://api.openai.com/v1/embeddings",
        body=vector,
        status=200,
    )
    embeddings.create([document])
    # Test
    documents = milvus.get_all_documents()
    # Check
    assert len(documents) == 1
    assert documents[0].meta["vector_id"] is not None


def test_embeddings_create_error_timeout(server, document):
    # Ensure embeddings.create handles OpenAI API errors.
    server.add(
        responses.POST,
        "https://api.openai.com/v1/embeddings",
        json={"error": "timeout"},
        status=408,
    )
    # Test
    with pytest.raises(AIError) as e:
        embeddings.create([document])
    # Check
    assert isinstance(e.value.original_exception, OpenAIError)


def test_embeddings_create_api_connection_error(server, document):
    # Ensure embeddings.create handles OpenAI API errors.
    server.add(
        responses.POST,
        "https://api.openai.com/v1/embeddings",
        json={"error": "api error"},
        status=500,
    )
    # Test
    with pytest.raises(AIError) as e:
        embeddings.create([document])
    # Check
    assert isinstance(e.value.original_exception, OpenAIError)


def test_embeddings_create_client_error(server, document):
    # Ensure embeddings.create handles OpenAI API errors.
    server.add(
        responses.POST,
        "https://api.openai.com/v1/embeddings",
        json={"error": "bad request"},
        status=400,
    )
    # Test
    with pytest.raises(AIError) as e:
        embeddings.create([document])
    # Check
    assert isinstance(e.value.original_exception, OpenAIError)


def test_embeddings_create_authentication_error(server, document):
    # Ensure embeddings.create handles OpenAI API errors.
    server.add(
        responses.POST,
        "https://api.openai.com/v1/embeddings",
        json={"error": "auth error"},
        status=401,
    )
    # Test
    with pytest.raises(AIError) as e:
        embeddings.create([document])
    # Check
    assert isinstance(e.value.original_exception, OpenAIError)


def test_embeddings_create_permission_error(server, document):
    # Ensure embeddings.create handles OpenAI API errors.
    server.add(
        responses.POST,
        "https://api.openai.com/v1/embeddings",
        json={"error": "permission error"},
        status=403,
    )
    # Test
    with pytest.raises(AIError) as e:
        embeddings.create([document])
    # Check
    assert isinstance(e.value.original_exception, OpenAIError)


def test_embeddings_create_rate_limit_error(server, document):
    # Ensure embeddings.create handles OpenAI API errors.
    server.add(
        responses.POST,
        "https://api.openai.com/v1/embeddings",
        json={"error": "rate limit"},
        status=429,
    )
    # Test
    with pytest.raises(AIError) as e:
        embeddings.create([document])
    # Check
    assert isinstance(e.value.original_exception, OpenAIError)
