# Build Plan

## Product goal

Turn a YouTube URL into a short, readable summary with key points and source timestamps.

## Stage 1: Deterministic input pipeline

- Support watch, short, embed, and `youtu.be` URL forms.
- Extract and validate the 11-character video ID.
- Fetch transcript snippets with `YouTubeTranscriptApi().fetch(video_id)`.
- Normalize snippets into text while preserving timestamps.
- Add tests for URL variants and transcript normalization using fakes.

## Stage 2: Prompt experiments

- Save representative transcript fixtures locally.
- Define several prompt variants with the same output requirements.
- Record prompt version, model, input size, output, and evaluation notes.
- Compare factuality, concision, structure, and timestamp usefulness.

## Stage 3: OpenAI automation

- Add an OpenAI client adapter that receives a transcript and prompt version.
- Keep the API key in an environment variable; never commit it.
- Add chunking for transcripts that exceed the selected model's context budget.
- Parse model output into a stable summary schema.
- Add retry, timeout, and provider-error handling.

## Stage 4: User-facing workflow

- Add a CLI first: `python -m youtube_summarizer <youtube-url>`.
- Add optional JSON output for downstream tools.
- Add a web UI only after the command-line workflow is reliable.

## Research and constraints

- Confirm which transcript languages to prefer.
- Handle unavailable, disabled, translated, and generated transcripts explicitly.
- Respect YouTube terms, provider terms, rate limits, and copyright constraints.
- Decide whether transcript and summary data should be retained locally.

## Acceptance checks

- URL parsing is deterministic and has no network dependency.
- Transcript retrieval receives a video ID, never a full URL.
- Prompt variants can be evaluated against the same fixture.
- OpenAI credentials are not present in source files or logs.
- A failed transcript or model request produces an actionable error.
