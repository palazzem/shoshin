import os
from pathlib import Path

import click
from haystack.utils import convert_files_to_docs

from shoshin import ai
from shoshin.conf import settings as s
from shoshin.exceptions import AIError, AudioExtractionError
from shoshin.pipeline import embeddings, processors


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

    try:
        processors.extract_audio_from_video(video_file, output)
    except AudioExtractionError as e:
        raise click.ClickException(e)

    click.echo(f"Audio track converted to: {output}")


@cli.command()
@click.argument("audio_file")
@click.option("--output", help="Output file name (default: <audio_file>.txt)")
def transcribe(audio_file: str, output: str):
    _, ext = os.path.splitext(audio_file)
    ext = ext.lower()
    if ext != ".mp3":
        raise ValueError(f"Unsupported file type {ext}. Only .mp3 audio files are supported.")

    # If no output file name is provided, use the video file name with an MP3 extension.
    if output is None:
        output = Path(audio_file).stem + ".txt"

    # Save the transcription to a file.
    try:
        processors.transcribe_speech_to_text(audio_file, output)
    except AIError as e:
        raise click.ClickException(e)

    click.echo(f"Audio transcript saved in: {output}")


@cli.command()
@click.argument("transcriptions_folder")
@click.option("--language", default=s.DEFAULT_LANGUAGE, show_default=True, help="Transcriptions language")
@click.option("--no-progress", default=False, is_flag=True, show_default=True, help="Disable progress bar")
def embeddings_load(transcriptions_folder: str, language: str, disable_progress_bar: bool):
    # Update settings (progress bar)
    s.PROGRESS_BAR = not disable_progress_bar

    # Convert transcriptions to Haystack documents
    click.echo("Loading transcriptions into memory...")
    all_docs = convert_files_to_docs(dir_path=transcriptions_folder)

    # Preprocess documents using Haystack pre-processors
    click.echo("Cleaning documents...")
    documents = processors.clean_documents(all_docs, language)

    # Write documents into Document Store and generate embeddings through OpenAI
    click.echo(f"Create embeddings for {len(documents)} documents...")
    embeddings.create(documents)
    click.echo("Embeddings updated!")


@cli.command()
@click.argument("question")
def query(question: str):
    click.echo(ai.query(question))


if __name__ == "__main__":
    cli()
