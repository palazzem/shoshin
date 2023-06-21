import pytest
import responses
from haystack.errors import OpenAIError
from haystack.nodes import EmbeddingRetriever
from milvus_documentstore import MilvusDocumentStore

from shoshin.datastore.documents import DocumentStore
from shoshin.exceptions import AIError


def test_datastore_defaults(settings):
    # Ensure DocumentStore defaults are set correctly.
    settings.DOCUMENTS_INDEX = "test_index_name"
    # Test
    ds = DocumentStore()
    # Check
    assert isinstance(ds._store, MilvusDocumentStore)
    assert isinstance(ds._retriever, EmbeddingRetriever)
    assert ds._store.index == "test_index_name"


def test_datastore_different_index():
    # Ensure DocumentStore overrides index defaults.
    # Test
    ds = DocumentStore(index="test")
    # Check
    assert ds._store.index == "test"


def test_datastore_property_retriever():
    # Ensure DocumentStore exposes the underlying `EmbeddingRetriever`.
    # Test
    ds = DocumentStore()
    # Check
    assert ds.retriever is ds._retriever


def test_datastore_create_embeddings(document_store_mock, document):
    # Ensure embeddings.create stores the embedding in the document store.
    ds = document_store_mock
    # Test
    ds.create_embeddings([document])
    # Check
    assert ds._store.write_documents.call_count == 1
    assert ds._store.update_embeddings.call_count == 1
    ds._store.write_documents.assert_called_with([document])
    ds._store.update_embeddings.assert_called_with(ds._retriever)


def test_embeddings_create(document_store, document, server, vector):
    # Integration test for create_embeddings.
    ds = document_store
    server.add(
        responses.POST,
        "https://api.openai.com/v1/embeddings",
        body=vector,
        status=200,
    )
    # Test
    ds.create_embeddings([document])
    # Check
    documents = ds._store.get_all_documents()
    assert len(documents) == 1
    assert documents[0].meta["vector_id"] is not None


def test_embeddings_create_exception(document_store_mock, document):
    # Ensure exceptions are wrapped in AIError.
    ds = document_store_mock
    openai_error = OpenAIError(
        "OpenAI returned an error.\nStatus code: 400\nResponse body: ClientError",
        status_code=400,
    )
    ds._store.update_embeddings.side_effect = openai_error
    # Test
    with pytest.raises(AIError) as e:
        ds.create_embeddings([document])
    # Check
    assert isinstance(e.value.original_exception, OpenAIError)
    documents = ds._store.get_all_documents()
    assert len(documents) == 0
