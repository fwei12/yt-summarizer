# YouTube Video Summarizer

An intentionally small Python skeleton for turning a YouTube link into a concise summary with key points.

## Workflow

1. Extract the YouTube video ID with a regular expression.
2. Fetch timestamped transcript snippets with `youtube-transcript-api`.
3. Experiment with prompt variants against a saved transcript fixture.
4. Use the OpenAI Python SDK to automate the selected prompt.

## Layout

- `src/youtube_summarizer/youtube.py`: URL parsing and video ID extraction.
- `src/youtube_summarizer/transcript.py`: transcript provider boundary.
- `src/youtube_summarizer/prompts.py`: prompt experiment registry.
- `src/youtube_summarizer/openai_summarizer.py`: OpenAI provider boundary.
- `src/youtube_summarizer/cli.py`: future command-line entry point.
- `tests/`: focused tests that do not require network access or API keys.
- `docs/PLAN.md`: implementation stages and research questions.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

The provider integrations are intentionally incomplete. Read `docs/PLAN.md` before wiring credentials or making network calls.
