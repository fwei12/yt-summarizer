"""Transcript retrieval and normalization boundary."""

import os
from dataclasses import dataclass
from typing import List, Sequence


@dataclass(frozen=True)
class TranscriptSnippet:
    text: str
    start_seconds: float
    duration_seconds: float


def _proxy_config_from_env():
    """Build a Webshare proxy config when credentials are present."""
    username = os.getenv("WEBSHARE_PROXY_USERNAME")
    password = os.getenv("WEBSHARE_PROXY_PASSWORD")

    if username and password:
        from youtube_transcript_api.proxies import WebshareProxyConfig

        return WebshareProxyConfig(
            proxy_username=username,
            proxy_password=password,
        )

    http_url = (
        os.getenv("YOUTUBE_PROXY_HTTP")
        or os.getenv("HTTP_PROXY")
        or os.getenv("http_proxy")
    )
    https_url = (
        os.getenv("YOUTUBE_PROXY_HTTPS")
        or os.getenv("HTTPS_PROXY")
        or os.getenv("https_proxy")
    )

    if not http_url and not https_url:
        return None

    from youtube_transcript_api.proxies import GenericProxyConfig

    return GenericProxyConfig(
        http_url=http_url or https_url,
        https_url=https_url or http_url,
    )


def fetch_transcript(video_id: str, languages: Sequence[str] = ("en",)) -> List[TranscriptSnippet]:
    """Fetch a video's transcript using youtube-transcript-api.

    The dependency import is local so URL parsing and prompt tests do not require
    network dependencies or credentials.
    """
    from youtube_transcript_api import YouTubeTranscriptApi

    proxy_config = _proxy_config_from_env()
    client_kwargs = {"proxy_config": proxy_config} if proxy_config is not None else {}

    try:
        fetched = YouTubeTranscriptApi(**client_kwargs).fetch(video_id, languages=list(languages))
    except Exception as exc:  # pragma: no cover - network behavior is environment dependent
        message = str(exc)
        if "407" in message or "Proxy Authentication Required" in message:
            raise RuntimeError(
                "Webshare rejected the proxy credentials. Use the separate Proxy Username "
                "and Proxy Password from Webshare proxy settings, not your Webshare login email "
                "or account password."
            ) from exc
        if "429" in message or "Too Many Requests" in message:
            raise RuntimeError(
                "YouTube rate-limited the proxy while fetching the transcript. Use a Webshare "
                "residential proxy with rotation enabled, wait, or try again with a different "
                "proxy location."
            ) from exc
        if "RequestBlocked" in message or "IpBlocked" in message or "blocked" in message.lower():
            raise RuntimeError(
                "YouTube blocked this IP while fetching the transcript. Use a residential proxy via "
                "WebshareProxyConfig with WEBSHARE_PROXY_USERNAME and WEBSHARE_PROXY_PASSWORD, "
                "or provide a working proxy in HTTP_PROXY/HTTPS_PROXY."
            ) from exc
        raise

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
