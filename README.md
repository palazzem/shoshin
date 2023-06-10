# Shoshin

Conversational AI that gets context from a video course and provides teaching support to students, with an attitude of
openness, eagerness, and lack of preconceptions, just as a beginner would.

## Status

Project is under development.

## Requirements

- Python 3.11
- `ffmpeg` (for video to audio processing)

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
