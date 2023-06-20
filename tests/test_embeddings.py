import responses

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
