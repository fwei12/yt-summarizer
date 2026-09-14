import pytest

from youtube_summarizer.youtube import InvalidYouTubeUrl, extract_video_id


@pytest.mark.parametrize(
    "url",
    [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ?t=10",
        "https://www.youtube.com/shorts/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
    ],
)
def test_extract_video_id(url: str) -> None:
    assert extract_video_id(url) == "dQw4w9WgXcQ"


def test_extract_video_id_rejects_non_youtube_url() -> None:
    with pytest.raises(InvalidYouTubeUrl):
        extract_video_id("https://example.com/watch?v=dQw4w9WgXcQ")
