import os
from pathlib import Path

import click
from haystack.nodes import PreProcessor
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
    all_docs = convert_files_to_docs(dir_path=transcriptions_folder)
    click.echo("Transcriptions folder loaded into memory...")

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
    ds = MilvusDocumentStore()
    click.echo("Indexing data into Vector Database...")
    ds.write_documents(documents)
    click.echo("Documents loaded into Vector Database (index only).")


if __name__ == "__main__":
    cli()
