# Shoshin

Conversational AI that gets context from a video course and provides teaching support to students, with an attitude of
openness, eagerness, and lack of preconceptions, just as a beginner would.

## Requirements

- Python 3.11
- `ffmpeg` (for video to audio processing)

## Status

Project is under development. Installation requires to clone the repository and install the project in editable mode.

## Getting Started

This open-source project provides a Command-Line Interface (CLI) application, `shoshin`, dedicated to processing video files.
It leverages external APIs, thus requiring certain environment variables to be configured.

### Pre-requisites

Set up the necessary environment variables as follows:

```bash
OPENAI_API_KEY=<insert-your-openai-api-key-here>
```

### Using the `shoshin` CLI

The `shoshin` command enables various video processing operations:

```bash
Usage: shoshin [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  convert      Converts video files to audio
  transcribe   Transcribes audio files to text
```

#### Examples of usage:

Here are a few examples demonstrating how to use `shoshin`:

```bash
# Convert a video file to an audio file
$ shoshin convert video/lesson01.mp4 --output audio/lesson01.mp3

# Transcribe an audio file to a text file
$ shoshin transcribe audio/lesson01.mp3 --output text/lesson01.txt
```

In the examples above, the `convert` command extracts the audio from the specified video, while the `transcribe` command
generates a text transcription from an audio file. The `--output` option indicates where the resulting file should be saved.

## Development

We welcome external contributions, even though the project was initially intended for personal use. If you think some
parts could be exposed with a more generic interface, please open a GitHub issue to discuss your suggestion.

### Dev Environment

To create a virtual environment and install the project and its dependencies, execute the following command in your
terminal:

```bash
# Create and activate a new virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install all projects and their dependencies
pip install --upgrade pip
pip install -e '.[dev]'
```

Finally, install the pre-commit hooks:

```bash
pre-commit install
```
