from typing import List

import ffmpeg
import openai
from ffmpeg import Error
from haystack.nodes import PreProcessor
from haystack.schema import Document
from openai.error import OpenAIError

from ..conf import constants as c
from ..exceptions import AIError, AudioExtractionError


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


def transcribe_speech_to_text(audio_file: str, output_file: str) -> None:
    """Transcribes speech from an audio file using the OpenAI Whisper model.

    Args:
        audio_file (str): The path to the input audio file.
        output_file (str): The path to save the output text file.

    Raises:
        AIError: If the OpenAI API request fails for any reason.

    Returns:
        None
    """
    try:
        # Transcribe
        with open(audio_file, "rb") as stream:
            response = openai.Audio.transcribe("whisper-1", stream)

        # Save the transcription to a file
        with open(output_file, "w") as f:
            f.write(response["text"])
    except OpenAIError as e:
        # Catch-all for OpenAI errors. This is a temporary solution until we
        # implement different error handlers for different types of errors.
        # Tests are covering all possible OpenAI errors.
        raise AIError(e)
    except FileNotFoundError as e:
        raise e


def clean_documents(documents: List[Document], language: str, progress_bar: bool = False) -> List[Document]:
    """Preprocesses a list of documents according to the specified language.

    This function uses built-in Haystack preprocessors to clean up the documents, preparing them
    for the subsequent stages of the processing pipeline. Preprocessing involves removing empty lines,
    trimming white spaces, and splitting by word respecting sentence boundaries.

    Different languages can result in different word splits.

    Args:
        documents (List[Document]): The documents that need to be preprocessed.
        language (str): The language used for preprocessing.

    Returns:
        List[Document]: A list of preprocessed documents.
    """
    preprocessor = PreProcessor(
        language=language,
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        progress_bar=progress_bar,
        split_by="word",
        split_length=c.PREPROCESSOR_SPLIT_LENGTH,
        split_respect_sentence_boundary=True,
    )
    return preprocessor.process(documents)
