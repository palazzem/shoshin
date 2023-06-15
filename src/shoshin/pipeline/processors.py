import ffmpeg
from ffmpeg import Error

from ..conf import constants as c
from ..exceptions import AudioExtractionError


def extract_audio_from_video(video_file: str, output_file: str) -> None:
    """Extracts the audio from a video file and saves it as an MP3 file. Audio is
    downsampled to 16kHz as it is only used for speech recognition.

    TODO: use `pydub` to split on silence if lenght is > 25MB (Whisper API limit)

    Args:
        video_file (str): The path to the input video file.
        output_file (str): The path to save the output MP3 file.

    Raises:
        AudioExtractionError: If an error occurs during audio extraction.

    Returns:
        None
    """
    try:
        stream = ffmpeg.input(video_file)
        stream = ffmpeg.output(stream.audio, output_file, format="mp3", ar=c.AUDIO_SAMPLE_RATE)
        ffmpeg.run(stream, overwrite_output=True)
    except Error as e:
        raise AudioExtractionError(e)
