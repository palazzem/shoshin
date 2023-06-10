import os
from pathlib import Path

import click
from ffmpeg import Error

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

    try:
        utils.extract_audio(video_file, output)
    except Error as e:
        raise click.ClickException(f"Error occurred during audio extraction: {e}")

    click.echo(f"Audio extracted to: {output}")


@cli.command()
@click.argument("audio_file")
def transcribe(audio_file: str):
    _, ext = os.path.splitext(audio_file)
    ext = ext.lower()

    if ext != ".mp3":
        raise ValueError(f"Unsupported file type {ext}. Only .mp3 audio files are supported.")

    result = utils.speech_to_text(audio_file)
    click.echo(result)


if __name__ == "__main__":
    cli()
