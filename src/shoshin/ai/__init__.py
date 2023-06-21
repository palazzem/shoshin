from haystack.nodes import EmbeddingRetriever, PromptNode
from haystack.pipelines import GenerativeQAPipeline

from ..conf import constants as c
from ..conf import settings as s
from .prompts import lfqa


def query(retriever: EmbeddingRetriever, question: str) -> str:
    """Processes the given question through a generative QA pipeline and returns the answer.

    This function creates a PromptNode with specific parameters including the OpenAI API key and a
    default prompt template, and uses the given EmbeddingRetriever to construct a GenerativeQAPipeline.
    It then runs this pipeline with the provided question and a set parameter for the number of
    top retriever results to consider. The results of the pipeline run are returned.

    Args:
        retriever (EmbeddingRetriever): An instance of EmbeddingRetriever to be used in the generative
                                        QA pipeline for retrieving relevant documents.
        question (str): The question to be processed by the generative QA pipeline.

    Returns:
        str: The result from running the question through the generative QA pipeline.
    """
    prompt_node = PromptNode(
        model_name_or_path=c.LLM_MODEL,
        api_key=s.OPENAI_API_KEY,
        default_prompt_template=lfqa,
        max_length=s.PROMPT_MAX_TOKENS,
    )

    pipeline = GenerativeQAPipeline(generator=prompt_node, retriever=retriever)
    return pipeline.run(query=question, params={"Retriever": {"top_k": c.RETRIEVER_TOP_K}})["results"]
