import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from pydantic import ValidationError

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.playback.models import PlaybackOptions
from app.services.playback.service import run_playback

def test_run_playback_continuous_routing(tmp_path) -> None:
    manifest_path = tmp_path / "live_manifest.json"
    manifest_path.write_text("{}")  # Dummy content
    
    options = PlaybackOptions(
        manifest_path=str(manifest_path),
        mode="continuous",
        min_ready_chunks=2,
        poll_interval=0.1
    )
    
    mock_queue_instance = MagicMock()
    mock_player_instance = MagicMock()
    mock_player_instance.played_indices = [0, 1]
    
    with patch("app.services.playback.service.read_live_manifest") as mock_read, \
         patch("app.services.playback.service.AudioQueue", return_value=mock_queue_instance) as mock_queue_cls, \
         patch("app.services.playback.service.ContinuousPlayer", return_value=mock_player_instance) as mock_player_cls:
         
        mock_read.return_value.job_id = "job-123"
        
        state = run_playback(options)
        
        # Verify continuous path classes were instantiated and run
        mock_queue_cls.assert_called_once_with(
            manifest_path=Path(options.manifest_path),
            min_ready_chunks=2,
            poll_interval=0.1,
            idle_timeout=60.0
        )
        mock_player_cls.assert_called_once_with(mock_queue_instance)
        mock_player_instance.play.assert_called_once()
        
        assert state.status == "completed"
        assert state.played_chunk_count == 2
        assert state.played_chunk_indices == [0, 1]
        assert state.job_id == "job-123"

def test_run_playback_legacy_routing(tmp_path) -> None:
    manifest_path = tmp_path / "live_manifest.json"
    manifest_path.write_text("{}")
    
    options = PlaybackOptions(
        manifest_path=str(manifest_path),
        mode="legacy",
        poll_interval=0.1
    )
    
    mock_watcher_instance = MagicMock()
    chunk0 = MagicMock(index=0, start_seconds=0.0, end_seconds=30.0, instrumental_path="inst0.wav")
    mock_watcher_instance.watch.return_value = [chunk0]
    
    with patch("app.services.playback.service.read_live_manifest") as mock_read, \
         patch("app.services.playback.service.ManifestWatcher", return_value=mock_watcher_instance) as mock_watcher_cls, \
         patch("app.services.playback.service.play_chunk") as mock_play_chunk:
         
        mock_read.return_value.job_id = "job-abc"
        
        state = run_playback(options)
        
        # Verify legacy path components were used
        mock_watcher_cls.assert_called_once_with(Path(options.manifest_path), 0.1, 60.0)
        mock_play_chunk.assert_called_once_with(Path("inst0.wav"), None)
        
        assert state.status == "completed"
        assert state.played_chunk_count == 1
        assert state.played_chunk_indices == [0]
        assert state.job_id == "job-abc"

def test_playback_options_rejects_unknown_mode(tmp_path) -> None:
    manifest_path = tmp_path / "live_manifest.json"

    with pytest.raises(ValidationError):
        PlaybackOptions(
            manifest_path=str(manifest_path),
            mode="continous",
        )
