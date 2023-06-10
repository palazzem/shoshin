import ffmpeg


def extract_audio(video_file: str, output_file: str) -> None:
    """
    Extracts the audio from a video file and saves it as an MP3 file. Audio is downsampled to 16kHz
    as it is only used for speech recognition.

    TODO: use `pydub` to split on silence if lenght is > 25MB (Whisper API limit)

    Args:
        video_file (str): The path to the input video file.
        output_file (str): The path to save the output MP3 file.

    Raises:
        subprocess.CalledProcessError: If the FFmpeg command fails.

    Returns:
        None
    """
    stream = ffmpeg.input(video_file)
    stream = ffmpeg.output(stream.audio, output_file, format="mp3", ar=16000)
    ffmpeg.run(stream, overwrite_output=False)


def speech_to_text(audio_file: str) -> str:
    return "Audio has not been transcribed yet."
