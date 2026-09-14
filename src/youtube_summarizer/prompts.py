"""Prompt variants for controlled summarization experiments."""

from typing import Dict


PROMPTS: Dict[str, str] = {
    "concise": (
        "Summarize the transcript in 3-5 sentences. Then list 3-5 key points. "
        "Use only information supported by the transcript.\n\nTranscript:\n{transcript}"
    ),
    "structured": (
        "Return exactly these sections: Overview, Key points, and Open questions. "
        "Keep the response concise and distinguish facts from uncertainty.\n\n"
        "Transcript:\n{transcript}"
    ),
    "timestamps": (
        "Summarize the transcript with concise key points. For each key point, "
        "include the nearest useful timestamp in [MM:SS] format. Do not invent "
        "timestamps.\n\nTranscript:\n{transcript}"
    ),
}


def render_prompt(name: str, transcript: str) -> str:
    """Render a named prompt variant for one transcript."""
    try:
        template = PROMPTS[name]
    except KeyError as error:
        raise ValueError(f"Unknown prompt variant: {name}") from error
    return template.format(transcript=transcript)
