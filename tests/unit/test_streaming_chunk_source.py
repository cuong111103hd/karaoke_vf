import pytest
import sys
import time
import wave
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src folder to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.live.streaming_source import YouTubeStreamingChunkSource
from app.services.errors import DownloadError

@pytest.fixture
def source() -> YouTubeStreamingChunkSource:
    return YouTubeStreamingChunkSource("https://youtube.com/watch?v=xyz", "test-job-123", initial_buffer_seconds=2.0)

def test_streaming_source_prepare(source) -> None:
    fake_metadata = {"title": "Test Title", "duration": 120}
    fake_headers = {"User-Agent": "TestAgent"}
    with patch("app.services.live.streaming_source.get_youtube_audio_stream_info", return_value=("https://stream.url", fake_metadata, fake_headers)) as mock_resolve:
        path, metadata, markers, durations = source.prepare()
        
        assert path is None
        assert metadata == fake_metadata
        assert source.stream_url == "https://stream.url"
        assert source.http_headers == fake_headers
        assert "stream_info_resolve_started_at" in markers
        assert "stream_info_resolve_completed_at" in markers
        assert "stream_info_resolve_seconds" in durations
        mock_resolve.assert_called_once_with("https://youtube.com/watch?v=xyz")

def test_streaming_source_start_and_stop(source) -> None:
    source.stream_url = "https://stream.url"
    source.http_headers = {"User-Agent": "TestAgent", "Referer": "TestReferer"}
    
    mock_process = MagicMock(spec=subprocess.Popen)
    mock_process.stdout = MagicMock()
    mock_process.stdout.read.return_value = b""
    mock_process.stderr = MagicMock()
    mock_process.stderr.readline.return_value = b""
    mock_process.poll.return_value = None
    
    with patch("subprocess.Popen", return_value=mock_process) as mock_popen:
        source.start()
        
        mock_popen.assert_called_once()
        args, kwargs = mock_popen.call_args
        cmd = args[0]
        # Verify headers were formatted and passed before -i
        assert "-headers" in cmd
        headers_idx = cmd.index("-headers")
        assert cmd[headers_idx + 1] == "User-Agent: TestAgent\r\nReferer: TestReferer\r\n"
        assert cmd[headers_idx + 2] == "-i"
        
        assert source._is_running is True
        assert source._process is mock_process
        
        source.stop()
        assert source._is_running is False
        assert source._process is None
        mock_process.terminate.assert_called_once()

def test_streaming_source_wait_for_chunk_success(source, tmp_path) -> None:
    source.stream_url = "https://stream.url"
    output_wav = tmp_path / "chunk_0.wav"
    
    # 1 second of audio at 176,400 bytes/sec is 176,400 bytes
    mock_pcm_data = b"\x00\x01" * 88200 # 176400 bytes
    
    mock_process = MagicMock(spec=subprocess.Popen)
    mock_process.stdout = MagicMock()
    mock_process.stdout.read.side_effect = [mock_pcm_data, b""]
    mock_process.stderr = MagicMock()
    mock_process.stderr.readline.return_value = b""
    mock_process.poll.return_value = None
    
    with patch("subprocess.Popen", return_value=mock_process):
        source.start()
        
        # Wait for chunk 0 (0.0s to 1.0s). Should only require 1.0s * 176,400 bytes.
        source.wait_for_chunk(0, 0.0, 1.0, output_wav)
        
        assert output_wav.exists()
        with wave.open(str(output_wav), "rb") as w:
            assert w.getnchannels() == 2
            assert w.getsampwidth() == 2
            assert w.getframerate() == 44100
            assert w.getnframes() == 44100
            
        assert "first_source_chunk_ready_at" in source.timing_markers
        
        source.stop()

def test_streaming_source_ffmpeg_early_exit(source, tmp_path) -> None:
    source.stream_url = "https://stream.url"
    output_wav = tmp_path / "chunk_0.wav"
    
    mock_process = MagicMock(spec=subprocess.Popen)
    mock_process.stdout = MagicMock()
    mock_process.stdout.read.return_value = b""
    mock_process.stderr = MagicMock()
    mock_process.stderr.readline.side_effect = [b"ffmpeg configuration error\n", b""]
    mock_process.poll.return_value = 1
    mock_process.returncode = 1
    
    with patch("subprocess.Popen", return_value=mock_process):
        source.start()
        
        with pytest.raises(DownloadError) as exc_info:
            source.wait_for_chunk(0, 0.0, 1.0, output_wav)
            
        assert "ffmpeg exited early with code 1" in str(exc_info.value)
        assert "ffmpeg configuration error" in str(exc_info.value)
        
        source.stop()

def test_streaming_source_wait_timeout(source, tmp_path) -> None:
    source.stream_url = "https://stream.url"
    source.chunk_wait_timeout_seconds = 0.1
    output_wav = tmp_path / "chunk_0.wav"
    
    mock_process = MagicMock(spec=subprocess.Popen)
    mock_process.stdout = MagicMock()
    # Read blocks forever returning empty but without EOF if simulated via sleep
    mock_process.stdout.read.side_effect = lambda size: time.sleep(0.5) or b""
    mock_process.stderr = MagicMock()
    mock_process.stderr.readline.return_value = b""
    mock_process.poll.return_value = None
    
    with patch("subprocess.Popen", return_value=mock_process):
        source.start()
        
        with pytest.raises(DownloadError) as exc_info:
            source.wait_for_chunk(0, 0.0, 1.0, output_wav)
            
        assert "Timeout waiting for source chunk" in str(exc_info.value)
        source.stop()

def test_streaming_source_inactivity_timeout(source, tmp_path) -> None:
    source.stream_url = "https://stream.url"
    source.stream_inactivity_timeout_seconds = 0.1
    output_wav = tmp_path / "chunk_0.wav"
    
    mock_process = MagicMock(spec=subprocess.Popen)
    mock_process.stdout = MagicMock()
    # Simulate blocked stream read
    mock_process.stdout.read.side_effect = lambda size: time.sleep(0.5) or b""
    mock_process.stderr = MagicMock()
    mock_process.stderr.readline.return_value = b""
    mock_process.poll.return_value = None
    
    with patch("subprocess.Popen", return_value=mock_process):
        source.start()
        # Set last_pcm_at to a past time to trigger inactivity immediately
        source.last_pcm_at = time.time() - 1.0
        
        with pytest.raises(DownloadError) as exc_info:
            source.wait_for_chunk(0, 0.0, 1.0, output_wav)
            
        assert "Stream inactivity timeout" in str(exc_info.value)
        source.stop()

def test_streaming_source_discard_before(source, tmp_path) -> None:
    source.stream_url = "https://stream.url"
    output_wav = tmp_path / "chunk_1.wav"
    
    # 5 seconds of audio data: 5 * 176,400 = 882,000 bytes
    mock_pcm_data = b"\x01" * 882000
    
    mock_process = MagicMock(spec=subprocess.Popen)
    mock_process.stdout = MagicMock()
    mock_process.stdout.read.side_effect = [mock_pcm_data, b""]
    mock_process.stderr = MagicMock()
    mock_process.stderr.readline.return_value = b""
    mock_process.poll.return_value = None
    
    with patch("subprocess.Popen", return_value=mock_process):
        source.start()
        
        # Read the mock data into buffer
        time.sleep(0.1)
        
        # Discard everything before 2.0s: 2.0 * 176400 = 352800 bytes
        source.discard_before(2.0)
        assert source._buffer_start_byte == 352800
        
        # Wait for chunk 1: from 2.0s to 4.0s (should extract relative 0 to 2.0s)
        # Required end is 4.0s relative to absolute beginning.
        # Relative end in buffer = 4.0 * 176400 - 352800 = 352800 bytes.
        source.wait_for_chunk(1, 2.0, 4.0, output_wav)
        
        assert output_wav.exists()
        with wave.open(str(output_wav), "rb") as w:
            assert w.getnframes() == 88200 # 2.0s * 44100
            
        source.stop()
