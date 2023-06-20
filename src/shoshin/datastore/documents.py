from typing import List, Optional, Union

from haystack.nodes import EmbeddingRetriever
from haystack.schema import Document
from milvus_documentstore import MilvusDocumentStore

from ..conf import constants as c
from ..conf import settings as s


class DocumentStore:
    """
    A wrapper class for `MilvusDocumentStore` that facilitates the management of document embeddings.

    The class is responsible for creating an instance of the `MilvusDocumentStore` and its corresponding
    `EmbeddingRetriever`. It also exposes methods to write documents to the store and update their embeddings.

    Attributes:
        retriever (EmbeddingRetriever): The Embedding Retriever instance.
    """

    def __init__(self, index: Optional[str] = None) -> None:
        """
        Creates a `DocumentStore` instance, initializing the `MilvusDocumentStore` and its corresponding
        EmbeddingRetriever.

        Args:
            index (str, optional): The index for the Document Store. Defaults to settings DOCUMENTS_INDEX.
        """
        # Settings
        self._index = index or s.DOCUMENTS_INDEX

        # Document Store
        self._store = MilvusDocumentStore(
            embedding_dim=c.EMBEDDING_DIM, sql_url=s.DATABASE_URL, progress_bar=s.PROGRESS_BAR, index=self._index
        )
        self._retriever = EmbeddingRetriever(
            api_key=s.OPENAI_API_KEY,
            document_store=self._store,
            embedding_model=c.EMBEDDING_MODEL,
            progress_bar=s.PROGRESS_BAR,
        )

    @property
    def retriever(self) -> EmbeddingRetriever:
        """
        Gets the `EmbeddingRetriever` instance associated with this `DocumentStore`.

        It is expected to use this retriever with a Generative Pipeline.

        Returns:
            `EmbeddingRetriever`: The `EmbeddingRetriever` instance.
        """
        return self._retriever

    def write_documents(self, documents: Union[List[dict], List[Document]]) -> None:
        """
        Writes documents to the underlying `MilvusDocumentStore`.

        Args:
            documents: The list of `Document` to write to the store.

        Returns:
            None.
        """
        self._store.write_documents(documents)

    def update_embeddings(self) -> None:
        """
        Updates embeddings in the Document Store using the associated `EmbeddingRetriever`.

        Returns:
            None.
        """
        self._store.update_embeddings(self._retriever)
