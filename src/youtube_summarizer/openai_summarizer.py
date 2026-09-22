"""OpenAI summarization boundary."""

import os

from openai import OpenAI

from youtube_summarizer.prompts import render_prompt


class SummarizationResult:
    """Structured output from the OpenAI summary step."""

    def __init__(self, raw_text: str, prompt_name: str, model: str) -> None:
        self.raw_text = raw_text
        self.prompt_name = prompt_name
        self.model = model


def summarize_with_openai(
    transcript: str,
    prompt_name: str = "concise",
    model: str = "",
) -> SummarizationResult:
    """Send the transcript through a prompt and return the summary text."""
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set. Add it to your environment or .env file.")

    prompt = render_prompt(prompt_name, transcript)
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model_name,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("OpenAI returned empty content for the transcript summary.")

    return SummarizationResult(
        raw_text=content.strip(),
        prompt_name=prompt_name,
        model=model_name,
    )
