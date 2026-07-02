import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src folder to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.integrations.youtube import get_youtube_audio_stream_info
from app.services.errors import DownloadError

def test_get_youtube_audio_stream_info_success() -> None:
    fake_info = {
        'url': 'https://youtube.com/stream.webm',
        'title': 'Test Song',
        'duration': 180,
        'uploader': 'Test Artist',
        'view_count': 1000,
        'webpage_url': 'https://youtube.com/watch?v=xyz',
        'http_headers': {'User-Agent': 'TestAgent'}
    }
    
    with patch("yt_dlp.YoutubeDL") as mock_ydl_class:
        mock_ydl = MagicMock()
        mock_ydl.extract_info.return_value = fake_info
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        
        stream_url, metadata, headers = get_youtube_audio_stream_info("https://youtube.com/watch?v=xyz")
        
        assert stream_url == "https://youtube.com/stream.webm"
        assert metadata["title"] == "Test Song"
        assert metadata["duration"] == 180
        assert metadata["uploader"] == "Test Artist"
        assert metadata["view_count"] == 1000
        assert metadata["webpage_url"] == "https://youtube.com/watch?v=xyz"
        assert headers == {'User-Agent': 'TestAgent'}
        mock_ydl.extract_info.assert_called_once_with("https://youtube.com/watch?v=xyz", download=False)

def test_get_youtube_audio_stream_info_missing_url() -> None:
    fake_info = {
        'title': 'Test Song'
    }
    with patch("yt_dlp.YoutubeDL") as mock_ydl_class:
        mock_ydl = MagicMock()
        mock_ydl.extract_info.return_value = fake_info
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        
        with pytest.raises(DownloadError) as exc_info:
            get_youtube_audio_stream_info("https://youtube.com/watch?v=xyz")
        assert "Could not find a direct audio URL" in str(exc_info.value)

def test_get_youtube_audio_stream_info_exception_translation() -> None:
    with patch("yt_dlp.YoutubeDL") as mock_ydl_class:
        mock_ydl = MagicMock()
        mock_ydl.extract_info.side_effect = RuntimeError("Network error")
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        
        with pytest.raises(DownloadError) as exc_info:
            get_youtube_audio_stream_info("https://youtube.com/watch?v=xyz")
        assert "Error resolving YouTube stream URL" in str(exc_info.value)
        assert isinstance(exc_info.value.original_error, RuntimeError)
