"""Command-line entry point placeholder."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize a YouTube video")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--prompt", default="concise", help="Prompt variant name")
    parser.add_argument("--language", default="en", help="Preferred transcript language")
    parser.parse_args()
    raise NotImplementedError(
        "TODO: connect URL parsing, transcript retrieval, and OpenAI summarization"
    )


if __name__ == "__main__":
    main()
