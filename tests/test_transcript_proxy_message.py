import pytest

from youtube_summarizer.transcript import fetch_transcript


def test_fetch_transcript_shows_actionable_proxy_message(monkeypatch):
    class FakeApi:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def fetch(self, video_id, languages=None):
            raise RuntimeError("RequestBlocked: YouTube blocked this IP")

    import youtube_transcript_api

    monkeypatch.setattr(youtube_transcript_api, "YouTubeTranscriptApi", FakeApi)

    with pytest.raises(RuntimeError, match="Use a residential proxy"):
        fetch_transcript("dQw4w9WgXcQ")


def test_fetch_transcript_explains_proxy_authentication_failure(monkeypatch):
    class FakeApi:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def fetch(self, video_id, languages=None):
            raise RuntimeError("Tunnel connection failed: 407 Proxy Authentication Required")

    import youtube_transcript_api

    monkeypatch.setattr(youtube_transcript_api, "YouTubeTranscriptApi", FakeApi)

    with pytest.raises(RuntimeError, match="separate Proxy Username"):
        fetch_transcript("dQw4w9WgXcQ")


def test_fetch_transcript_explains_youtube_rate_limit(monkeypatch):
    class FakeApi:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def fetch(self, video_id, languages=None):
            raise RuntimeError("too many 429 error responses")

    import youtube_transcript_api

    monkeypatch.setattr(youtube_transcript_api, "YouTubeTranscriptApi", FakeApi)

    with pytest.raises(RuntimeError, match="rate-limited the proxy"):
        fetch_transcript("dQw4w9WgXcQ")
