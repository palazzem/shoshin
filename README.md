# Shoshin

[![Linting](https://github.com/palazzem/shoshin/actions/workflows/linting.yaml/badge.svg)](https://github.com/palazzem/shoshin/actions/workflows/linting.yaml)
[![Testing](https://github.com/palazzem/shoshin/actions/workflows/testing.yaml/badge.svg)](https://github.com/palazzem/shoshin/actions/workflows/testing.yaml)

Conversational AI that gets context from a video course and provides teaching support to students, with an attitude of
openness, eagerness, and lack of preconceptions, just as a beginner would.

## Requirements

- Python 3.11
- `ffmpeg` (for video to audio processing)
- `docker` and `docker compose` (for running Milvus vector database)

## Status

Project is under development. Installation requires to clone the repository and install the project in editable mode.
Follow the instructions in the [Development](#development) section.

## Getting Started

This open-source project provides a Command-Line Interface (CLI) application, `shoshin`, dedicated to processing video files.
It leverages external APIs, thus requiring certain environment variables to be configured.

### Using the `shoshin` CLI

The `shoshin` command enables various video processing operations:

```bash
Usage: shoshin [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  convert            Converts video files to audio
  transcribe         Transcribes audio files to text
  embeddings-load    Compute embeddings for all documents in a folder and load them into Milvus
  query              Create a question about indexed documents
```

#### Examples of usage:

Here are a few examples demonstrating how to use `shoshin`:

```bash
# Convert a video file to an audio file
$ shoshin convert video/lesson01.mp4 --output audio/lesson01.mp3

# Transcribe an audio file to a text file
$ shoshin transcribe audio/lesson01.mp3 --output text/lesson01.txt

# Load all documents in a folder into Milvus vector database
$ shoshin embeddings-load --language en transcriptions/

# Ask questions to the LLM that will be answered from the documents stored
$ shoshin query "What are the ethical implications of AI?"
```

The LLM prompt is instructed to use only indexed documents and not their knowledge base to avoid going off-track
from the video lessons.

During the `embeddings-load` is important to select a language via `--language` to ensure a better word split is done
for every document. Check [Haystack documentation](https://docs.haystack.deepset.ai/docs/languages) for more details.

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

# Install pre-commit hooks
pre-commit install

# Create folders and initial database to store documents metadata
mkdir -p audio video transcriptions volumes

# Set required environment variables
cp .env.development .env
```

Set up the necessary environment variables in the newly created `.env` file. All variables in there are required
for the project to run. You can see all available settings in the `shoshin/conf/settings.py` module.

Example of a `.env` file:
```bash
OPENAI_API_KEY=<insert-your-openai-api-key-here>
```

Finally, start required services to run Milvus vector database and PostgreSQL:

```bash
docker-compose up -d
```
