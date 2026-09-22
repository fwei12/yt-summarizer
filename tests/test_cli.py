import os

from youtube_summarizer import cli


def test_generate_summary_returns_openai_payload_when_available(monkeypatch):
    class FakeResult:
        def __init__(self, raw_text: str) -> None:
            self.raw_text = raw_text

    def fake_fetch(video_id, languages=("en",)):
        assert video_id == "dQw4w9WgXcQ"
        assert languages == ["en"]
        return [type("Snippet", (), {"text": "hello world", "start": 0, "duration": 2})()]

    monkeypatch.setattr(cli, "fetch_transcript", fake_fetch)
    monkeypatch.setattr(
        cli,
        "render_prompt",
        lambda name, transcript: f"PROMPT({name}): {transcript}",
    )
    monkeypatch.setattr(
        cli,
        "summarize_with_openai",
        lambda transcript, prompt_name, model: FakeResult(
            f"SUMMARY::{prompt_name}::{model}::{transcript}"
        ),
    )
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o-mini")

    result = cli.generate_summary(
        "https://youtu.be/dQw4w9WgXcQ",
        prompt_name="concise",
        language="en",
        webshare_username="user",
        webshare_password="pass",
    )

    assert result.startswith("SUMMARY::concise::gpt-4o-mini::")
    assert "hello world" in result
    assert os.environ["WEBSHARE_PROXY_USERNAME"] == "user"
    assert os.environ["WEBSHARE_PROXY_PASSWORD"] == "pass"
