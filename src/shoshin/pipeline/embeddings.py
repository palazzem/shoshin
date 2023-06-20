from typing import List

from haystack.errors import OpenAIError
from haystack.nodes import EmbeddingRetriever
from haystack.schema import Document
from milvus_documentstore import MilvusDocumentStore

from ..conf import constants as c
from ..conf import settings as s
from ..exceptions import AIError


def create(documents: List[Document]) -> None:
    """Writes a list of Document objects to the MilvusDocumentStore and updates their embeddings using
    OpenAI embeddings endpoints.

    This function initializes a MilvusDocumentStore with a given embedding dimension compatible with
    `text-embedding-ada-002`. Computing embeddings through this method requires an OpenAI API key as the
    embeddings generation is delegated to their models.

    Args:
        documents (List[Document]): A list of Document objects to be written into the MilvusDocumentStore.

    Raises:
        AIError: If the OpenAI API request fails for any reason.

    Returns:
        None

    Note:
        Using this function charges your OpenAI account.
    """
    # Write documents into Document Store
    ds = MilvusDocumentStore(embedding_dim=c.EMBEDDING_DIM, sql_url=s.DATABASE_URL, progress_bar=s.PROGRESS_BAR)
    ds.write_documents(documents)

    # Update embeddings through OpenAI embedding model
    retriever = EmbeddingRetriever(
        document_store=ds,
        embedding_model=c.EMBEDDING_MODEL,
        api_key=s.OPENAI_API_KEY,
        progress_bar=s.PROGRESS_BAR,
    )
    try:
        ds.update_embeddings(retriever)
    except OpenAIError as e:
        # Catch-all for OpenAI errors. This is a temporary solution until we
        # implement different error handlers for different types of errors.
        # Tests are covering all possible OpenAI errors.
        raise AIError(e)
