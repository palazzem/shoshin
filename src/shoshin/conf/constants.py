"""This module contains constants used throughout the application.

Constants:
    EMBEDDING_DIM (int): The dimensionality of the text embeddings.
    EMBEDDING_MODEL (str): The name of the text embedding model to use.
    LLM_MODEL (str): The name of the language model to use for text generation.
    PREPROCESSOR_SPLIT_LENGTH (int): The maximum length of text to process at once during preprocessing.
    RETRIEVER_TOP_K (int): The number of documents to retrieve from the index during a search.
"""
# LLM
# NOTE: `text-embedding-ada-002` has an output dimension of 1536
EMBEDDING_DIM = 1536
EMBEDDING_MODEL = "text-embedding-ada-002"
LLM_MODEL = "gpt-3.5-turbo"

# Haystack
PREPROCESSOR_SPLIT_LENGTH = 100
RETRIEVER_TOP_K = 10

# Processing
AUDIO_SAMPLE_RATE = 16000
