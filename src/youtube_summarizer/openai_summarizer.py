"""OpenAI summarization boundary."""

from typing import Any


class SummarizationResult:
    """Placeholder for a parsed, stable summary response."""

    def __init__(self, raw_text: str) -> None:
        self.raw_text = raw_text


def summarize_with_openai(
    transcript: str,
    prompt_name: str = "concise",
    model: str = "",
) -> SummarizationResult:
    """Call OpenAI with a selected prompt once the client policy is decided."""
    del transcript, prompt_name, model
    raise NotImplementedError(
        "TODO: initialize the OpenAI Python client, call the selected model, "
        "and parse the response into a stable summary schema"
    )
