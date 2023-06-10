import click
import ffmpeg
import openai
from ffmpeg import Error


def extract_audio(video_file: str, output_file: str) -> None:
    """Extracts the audio from a video file and saves it as an MP3 file. Audio is
    downsampled to 16kHz as it is only used for speech recognition.

    TODO: use `pydub` to split on silence if lenght is > 25MB (Whisper API limit)

    Args:
        video_file (str): The path to the input video file.
        output_file (str): The path to save the output MP3 file.

    Raises:
        click.ClickException: If an error occurs during audio extraction.

    Returns:
        None
    """
    try:
        stream = ffmpeg.input(video_file)
        stream = ffmpeg.output(stream.audio, output_file, format="mp3", ar=16000)
        ffmpeg.run(stream, overwrite_output=False)
    except Error as e:
        raise click.ClickException(f"Error occurred during audio extraction: {e}")


def speech_to_text(audio_file: str) -> str:
    """Transcribes speech from an audio file using the OpenAI Whisper model.

    Args:
        audio_file (str): The path to the input audio file.

    Raises:
        click.ClickException: If the OpenAI API request fails for any reason.

    Returns:
        str: The transcribed text.
    """
    stream = open(audio_file, "rb")
    try:
        return openai.Audio.transcribe("whisper-1", stream)["text"]
    except openai.error.Timeout as e:
        raise click.ClickException(f"OpenAI API request timed out: {e}")
    except openai.error.APIError as e:
        raise click.ClickException(f"OpenAI API returned an API Error: {e}")
    except openai.error.APIConnectionError as e:
        raise click.ClickException(f"OpenAI API request failed to connect: {e}")
    except openai.error.InvalidRequestError as e:
        raise click.ClickException(f"OpenAI API request was invalid: {e}")
    except openai.error.AuthenticationError as e:
        raise click.ClickException(f"OpenAI API request was not authorized: {e}")
    except openai.error.PermissionError as e:
        raise click.ClickException(f"OpenAI API request was not permitted: {e}")
    except openai.error.RateLimitError as e:
        raise click.ClickException(f"OpenAI API request exceeded rate limit: {e}")
