"""YouTube URL parsing."""

import re


_VIDEO_ID_PATTERN = re.compile(
    r"(?:youtube(?:-nocookie)?\.com/(?:watch\?(?:[^#\s]*?&)?v=|embed/|shorts/)|youtu\.be/)([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])",
    re.IGNORECASE,
)


class InvalidYouTubeUrl(ValueError):
    """Raised when a URL does not contain a valid YouTube video ID."""


def extract_video_id(url: str) -> str:
    """Extract an 11-character YouTube video ID from a supported URL."""
    match = _VIDEO_ID_PATTERN.search(url)
    if match is None:
        raise InvalidYouTubeUrl("Could not find a YouTube video ID in the URL")
    return match.group(1)
