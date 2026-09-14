"""Transcript retrieval and normalization boundary."""

from dataclasses import dataclass
from typing import List, Sequence


@dataclass(frozen=True)
class TranscriptSnippet:
    text: str
    start_seconds: float
    duration_seconds: float


def fetch_transcript(video_id: str, languages: Sequence[str] = ("en",)) -> List[TranscriptSnippet]:
    """Fetch a video's transcript using youtube-transcript-api.

    The dependency import is local so URL parsing and prompt tests do not require
    network dependencies or credentials.
    """
    from youtube_transcript_api import YouTubeTranscriptApi

    fetched = YouTubeTranscriptApi().fetch(video_id, languages=list(languages))
    return [
        TranscriptSnippet(
            text=snippet.text,
            start_seconds=snippet.start,
            duration_seconds=snippet.duration,
        )
        for snippet in fetched
    ]


def transcript_to_text(snippets: Sequence[TranscriptSnippet]) -> str:
    """Convert timestamped snippets into plain text for a prompt."""
    return " ".join(snippet.text.strip() for snippet in snippets if snippet.text.strip())
