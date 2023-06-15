import pytest
from ffmpeg import Error as FFMpegError

from shoshin.exceptions import AudioExtractionError
from shoshin.pipeline.processors import extract_audio_from_video


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
