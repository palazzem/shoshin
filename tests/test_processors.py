import pytest
import requests
import responses
from ffmpeg import Error as FFMpegError
from openai import error

from shoshin.exceptions import AIError, AudioExtractionError
from shoshin.pipeline.processors import (
    clean_documents,
    extract_audio_from_video,
    transcribe_speech_to_text,
)


def test_extract_audio_from_video(ffmpeg):
    # Ensure extract_audio_from_video calls ffmpeg correctly.
    extract_audio_from_video("video.mp4", "audio.mp3")
    ffmpeg.input.assert_called_with("video.mp4")
    ffmpeg.output.assert_called_with(ffmpeg.input().audio, "audio.mp3", format="mp3", ar=16000)
    assert ffmpeg.run.call_count == 1


def test_extract_audio_from_video_exception(ffmpeg):
    # Ensure extract_audio_from_video returns an exception.
    ffmpeg.run.side_effect = FFMpegError("ffmpeg", "stdout", "stderr")
    with pytest.raises(AudioExtractionError) as e:
        extract_audio_from_video("video.mp4", "audio.mp3")

    assert e.value.original_exception.args == ("ffmpeg error (see stderr output for detail)",)


def test_transcribe_speech_to_text(server, audio_file, output_file):
    # Ensure transcribe_speech_to_text calls the OpenAI API correctly.
    headers = {
        "Date": "Mon, 01 Jan 2023 12:00:00 GMT",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "openai-organization": "user-test",
        "openai-processing-ms": "100",
        "openai-version": "2020-10-01",
        "strict-transport-security": "max-age=15724800; includeSubDomains",
        "x-ratelimit-limit-requests": "50",
        "x-ratelimit-remaining-requests": "49",
        "x-ratelimit-reset-requests": "1.2s",
        "x-request-id": "<redacted>",
        "CF-Cache-Status": "DYNAMIC",
        "Server": "cloudflare",
        "CF-RAY": "<redacted>",
        "alt-svc": 'h3=":443"; ma=86400',
    }
    response = {"text": "Thanks for watching!"}
    server.add(
        responses.POST,
        "https://api.openai.com/v1/audio/transcriptions",
        json=response,
        headers=headers,
        status=200,
    )
    # Test
    transcribe_speech_to_text(audio_file, output_file)
    # Check
    assert output_file.read_text() == "Thanks for watching!"


def test_transcribe_speech_to_text_not_found(output_file):
    # Ensure transcribe_speech_to_text raises FileNotFound error if no audio file is found.
    with pytest.raises(FileNotFoundError):
        transcribe_speech_to_text("audio.mp3", output_file)


def test_transcribe_speech_to_text_error_timeout(server, audio_file, output_file):
    # Ensure transcribe_speech_to_text handles OpenAI API errors.
    server.add(
        responses.POST,
        "https://api.openai.com/v1/audio/transcriptions",
        body=requests.exceptions.Timeout("<reason>"),
        status=408,
    )
    # Test
    with pytest.raises(AIError) as e:
        transcribe_speech_to_text(audio_file, output_file)
    # Check
    assert isinstance(e.value.original_exception, error.Timeout)


def test_transcribe_speech_to_text_error_api_connection_error(server, audio_file, output_file):
    # Ensure transcribe_speech_to_text handles OpenAI API errors.
    server.add(
        responses.POST,
        "https://api.openai.com/v1/audio/transcriptions",
        body=requests.exceptions.RequestException("<reason>"),
        status=500,
    )
    # Test
    with pytest.raises(AIError) as e:
        transcribe_speech_to_text(audio_file, output_file)
    # Check
    assert isinstance(e.value.original_exception, error.APIConnectionError)


def test_transcribe_speech_to_text_error_api_error(server, audio_file, output_file):
    # Ensure transcribe_speech_to_text handles OpenAI API errors.
    response = "bad-parsing"
    server.add(
        responses.POST,
        "https://api.openai.com/v1/audio/transcriptions",
        json=response,
        status=400,
    )
    # Test
    with pytest.raises(AIError) as e:
        transcribe_speech_to_text(audio_file, output_file)
    # Check
    assert isinstance(e.value.original_exception, error.APIError)


def test_transcribe_speech_to_text_error_invalid_request(server, audio_file, output_file):
    # Ensure transcribe_speech_to_text handles OpenAI API errors.
    error_msg = {
        "error": {
            "code": 400,
            "message": "<reason>",
            "type": "invalid_request_error",
            "param": "something",
        }
    }
    server.add(
        responses.POST,
        "https://api.openai.com/v1/audio/transcriptions",
        json=error_msg,
        status=400,
    )
    # Test
    with pytest.raises(AIError) as e:
        transcribe_speech_to_text(audio_file, output_file)
    # Check
    assert isinstance(e.value.original_exception, error.InvalidRequestError)


def test_transcribe_speech_to_text_error_authentication(server, audio_file, output_file):
    # Ensure transcribe_speech_to_text handles OpenAI API errors.
    error_msg = {
        "error": {
            "code": 401,
            "message": "AuthError",
            "type": "authentication_error",
            "param": "something",
        }
    }
    server.add(
        responses.POST,
        "https://api.openai.com/v1/audio/transcriptions",
        json=error_msg,
        status=401,
    )
    # Test
    with pytest.raises(AIError) as e:
        transcribe_speech_to_text(audio_file, output_file)
    # Check
    assert isinstance(e.value.original_exception, error.AuthenticationError)


def test_transcribe_speech_to_text_error_permission(server, audio_file, output_file):
    # Ensure transcribe_speech_to_text handles OpenAI API errors.
    error_msg = {
        "error": {
            "code": 403,
            "message": "PermissionError",
            "type": "permission_error",
            "param": "something",
        }
    }
    server.add(
        responses.POST,
        "https://api.openai.com/v1/audio/transcriptions",
        json=error_msg,
        status=403,
    )
    # Test
    with pytest.raises(AIError) as e:
        transcribe_speech_to_text(audio_file, output_file)
    # Check
    assert isinstance(e.value.original_exception, error.PermissionError)


def test_transcribe_speech_to_text_error_rate_limit(server, audio_file, output_file):
    # Ensure transcribe_speech_to_text handles OpenAI API errors.
    error_msg = {
        "error": {
            "code": 429,
            "message": "RateLimit",
            "type": "permission_error",
            "param": "something",
        }
    }
    server.add(
        responses.POST,
        "https://api.openai.com/v1/audio/transcriptions",
        json=error_msg,
        status=429,
    )
    # Test
    with pytest.raises(AIError) as e:
        transcribe_speech_to_text(audio_file, output_file)
    # Check
    assert isinstance(e.value.original_exception, error.RateLimitError)


def test_clean_documents_success(document):
    # Ensure clean_documents returns a list of cleaned Documents
    document.content = "   This is an uncleaned statement. \n\n"
    # Test
    documents = clean_documents([document], "en", progress_bar=False)
    # Check
    assert len(documents) == 1
    assert documents[0].content == "This is an uncleaned statement."


def test_clean_documents_split(document):
    # Ensure clean_documents returns a multiple documents if the content is too long
    document.content = """
        This is a sample sentence in paragraph_1. This is a sample sentence in paragraph_1. This is a sample sentence in
        paragraph_1. This is a sample sentence in paragraph_1. This is a sample sentence in paragraph_1.\f

        This is a sample sentence in paragraph_2. This is a sample sentence in paragraph_2. This is a sample sentence in
        paragraph_2. This is a sample sentence in paragraph_2. This is a sample sentence in paragraph_2.

        This is a sample sentence in paragraph_3. This is a sample sentence in paragraph_3. This is a sample sentence in
        paragraph_3. This is a sample sentence in paragraph_3. This is to trick the test with using an abbreviation\f
        like Dr. in the sentence."""
    # Test
    documents = clean_documents([document], "en", progress_bar=False)
    # Check
    assert len(documents) == 2
    assert documents[0].meta["_split_id"] == 0
    assert documents[1].meta["_split_id"] == 1
