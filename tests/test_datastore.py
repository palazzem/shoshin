from haystack.nodes import EmbeddingRetriever
from milvus_documentstore import MilvusDocumentStore

from shoshin.datastore.documents import DocumentStore


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


def test_datastore_write_documents(document, document_store):
    # Ensure DocumentStore writes documents to the underlying `MilvusDocumentStore`.
    # Test
    document_store.write_documents([document])
    # Check
    assert document_store._store.write_documents.call_count == 1
    document_store._store.write_documents.assert_called_with([document])


def test_datastore_update_embeddings(document_store):
    # Ensure DocumentStore updates embeddings with the underlying `EmbeddingRetriever`.
    # Test
    document_store.update_embeddings()
    # Check
    assert document_store._store.update_embeddings.call_count == 1
    document_store._store.update_embeddings.assert_called_with(document_store._retriever)
