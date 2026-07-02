import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.live.models import LiveOptions
from app.services.live.source_factory import get_live_source
from app.services.live.youtube_source import YouTubeLiveSource
from app.services.live.streaming_source import YouTubeStreamingChunkSource

def test_source_factory_download() -> None:
    options = LiveOptions(
        youtube_url="https://youtube.com/watch?v=xyz",
        source_mode="download"
    )
    source = get_live_source("https://youtube.com/watch?v=xyz", "job-123", options)
    assert isinstance(source, YouTubeLiveSource)

def test_source_factory_streaming() -> None:
    options = LiveOptions(
        youtube_url="https://youtube.com/watch?v=xyz",
        source_mode="streaming"
    )
    source = get_live_source("https://youtube.com/watch?v=xyz", "job-123", options)
    assert isinstance(source, YouTubeStreamingChunkSource)
    assert source.initial_buffer_seconds == 20.0

def test_source_factory_invalid_mode_bypass_validation() -> None:
    # Construct options directly bypassing or overriding
    options = LiveOptions(
        youtube_url="https://youtube.com/watch?v=xyz",
    )
    # Force set an unsupported mode
    options.source_mode = "invalid_mode"
    with pytest.raises(ValueError) as exc_info:
        get_live_source("https://youtube.com/watch?v=xyz", "job-123", options)
    assert "Unsupported source mode" in str(exc_info.value)
