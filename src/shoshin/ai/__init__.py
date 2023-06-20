from haystack.nodes import EmbeddingRetriever, PromptNode
from haystack.pipelines import GenerativeQAPipeline
from milvus_documentstore import MilvusDocumentStore

from ..conf import constants as c
from ..conf import settings as s
from .prompts import lfqa


def query(question: str) -> str:
    ds = MilvusDocumentStore(embedding_dim=c.EMBEDDING_DIM, sql_url=s.DATABASE_URL)

    # Retriever
    retriever = EmbeddingRetriever(
        document_store=ds,
        embedding_model=c.EMBEDDING_MODEL,
        api_key=s.OPENAI_API_KEY,
    )

    # Node
    prompt_node = PromptNode(
        model_name_or_path=c.LLM_MODEL,
        api_key=s.OPENAI_API_KEY,
        default_prompt_template=lfqa,
        max_length=s.PROMPT_MAX_TOKENS,
    )

    pipeline = GenerativeQAPipeline(generator=prompt_node, retriever=retriever)
    return pipeline.run(query=question, params={"Retriever": {"top_k": c.RETRIEVER_TOP_K}})["results"]
