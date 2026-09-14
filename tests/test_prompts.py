from youtube_summarizer.prompts import render_prompt


def test_prompt_variant_includes_transcript() -> None:
    assert "sample transcript" in render_prompt("concise", "sample transcript")
