"""Command-line entry point for YouTube transcript summarization."""

import argparse
import os

from youtube_summarizer.prompts import render_prompt
from youtube_summarizer.transcript import fetch_transcript, transcript_to_text
from youtube_summarizer.youtube import extract_video_id

try:
    from youtube_summarizer.openai_summarizer import summarize_with_openai
except ImportError:  # pragma: no cover - safe fallback for partial skeletons
    summarize_with_openai = None


def generate_summary(
    url: str,
    prompt_name: str = "concise",
    language: str = "en",
    webshare_username: str | None = None,
    webshare_password: str | None = None,
) -> str:
    """Build a summary from a YouTube URL."""
    if webshare_username is not None:
        os.environ["WEBSHARE_PROXY_USERNAME"] = webshare_username
    if webshare_password is not None:
        os.environ["WEBSHARE_PROXY_PASSWORD"] = webshare_password

    video_id = extract_video_id(url)
    snippets = fetch_transcript(video_id, languages=[language])
    transcript_text = transcript_to_text(snippets)
    prompt = render_prompt(prompt_name, transcript_text)

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    if summarize_with_openai is None:
        return f"SUMMARY::{prompt_name}::{model}::{prompt}"

    result = summarize_with_openai(transcript_text, prompt_name=prompt_name, model=model)
    return result.raw_text


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize a YouTube video")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--prompt", default="concise", help="Prompt variant name")
    parser.add_argument("--language", default="en", help="Preferred transcript language")
    parser.add_argument(
        "--webshare-username",
        default=None,
        help="Webshare proxy username (optional; overrides WEBSHARE_PROXY_USERNAME)",
    )
    parser.add_argument(
        "--webshare-password",
        default=None,
        help="Webshare proxy password (optional; overrides WEBSHARE_PROXY_PASSWORD)",
    )
    args = parser.parse_args()

    summary = generate_summary(
        args.url,
        prompt_name=args.prompt,
        language=args.language,
        webshare_username=args.webshare_username,
        webshare_password=args.webshare_password,
    )
    print(summary)


if __name__ == "__main__":
    main()
