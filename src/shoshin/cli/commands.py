import os
from pathlib import Path

import click
from haystack.nodes import EmbeddingRetriever, PreProcessor, PromptNode, PromptTemplate
from haystack.pipelines import GenerativeQAPipeline
from haystack.utils import convert_files_to_docs
from milvus_documentstore import MilvusDocumentStore

from shoshin.cli import utils


@click.group()
def cli():
    pass


@cli.command()
@click.argument("video_file")
@click.option("--output", help="Output file name (default: <video_file>.mp3)")
def convert(video_file: str, output: str):
    _, ext = os.path.splitext(video_file)
    ext = ext.lower()
    if ext != ".mp4":
        raise ValueError(f"Unsupported file type {ext}. Only .mp4 video files are supported.")

    # If no output file name is provided, use the video file name with an MP3 extension.
    if output is None:
        output = Path(video_file).stem + ".mp3"

    utils.extract_audio(video_file, output)
    click.echo(f"Audio track converted to: {output}")


@cli.command()
@click.argument("audio_file")
@click.option("--output", help="Output file name (default: <video_file>.txt)")
def transcribe(audio_file: str, output: str):
    _, ext = os.path.splitext(audio_file)
    ext = ext.lower()
    if ext != ".mp3":
        raise ValueError(f"Unsupported file type {ext}. Only .mp3 audio files are supported.")

    # If no output file name is provided, use the video file name with an MP3 extension.
    if output is None:
        output = Path(audio_file).stem + ".txt"

    transcription = utils.speech_to_text(audio_file)

    # Save the transcription to a file.
    with open(output, "w") as f:
        f.write(transcription)

    click.echo(f"Audio transcript saved in: {output}")


@cli.command()
@click.argument("transcriptions_folder")
@click.option("--language", default="en", help="Language of the transcriptions (default: en)")
def embeddings_load(transcriptions_folder: str, language: str):
    # Convert transcriptions to Haystack documents
    click.echo("Loading transcriptions into memory...")
    all_docs = convert_files_to_docs(dir_path=transcriptions_folder)

    # Preprocess documents using the selected language
    preprocessor = PreProcessor(
        language=language,
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        split_by="word",
        split_length=100,
        split_respect_sentence_boundary=True,
    )
    documents = preprocessor.process(all_docs)

    # Write documents into Document Store
    # NOTE: `text-embedding-ada-002` has an output dimension of 1536
    ds = MilvusDocumentStore(embedding_dim=1536, sql_url="sqlite:///db.sqlite3")
    ds.write_documents(documents)
    click.echo(f"Documents loaded into the Vector Database: {len(documents)}")

    # Update embeddings through OpenAI embedding model
    retriever = EmbeddingRetriever(
        document_store=ds,
        embedding_model="text-embedding-ada-002",
        model_format="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    ds.update_embeddings(retriever)
    click.echo("Embeddings updated!")


@cli.command()
@click.argument("question")
def query(question: str):
    ds = MilvusDocumentStore(embedding_dim=1536, sql_url="sqlite:///db.sqlite3")

    # Retriever
    retriever = EmbeddingRetriever(
        document_store=ds,
        embedding_model="text-embedding-ada-002",
        model_format="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Prompt
    lfqa_prompt = PromptTemplate(
        name="lfqa",
        prompt_text="""Synthesize a comprehensive answer from the following text for the given question.
                       Provide a clear and concise response that summarizes the key points and information
                       presented in the text. Your answers must be in your own words. Always use Related
                       text before your knowledge base. If you don't find anything in the related text,
                       kindly mention what the course is about and that the question goes outside of the
                       scope of the video course.
                       \n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer:""",
    )
    prompt_node = PromptNode(
        model_name_or_path="gpt-3.5-turbo",
        api_key=os.getenv("OPENAI_API_KEY"),
        default_prompt_template=lfqa_prompt,
        max_length=2048,
    )
    pipeline = GenerativeQAPipeline(generator=prompt_node, retriever=retriever)

    output = pipeline.run(query=question, params={"Retriever": {"top_k": 10}})
    print(output["results"])


if __name__ == "__main__":
    cli()
