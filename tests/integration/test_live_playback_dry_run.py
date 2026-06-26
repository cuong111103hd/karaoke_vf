import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.playback.service import run_playback
from app.services.playback.models import PlaybackOptions
from app.services.live.models import LiveManifest, LiveChunkMetadata, LiveChunkStatus, LiveStreamStatus
from app.services.live.manifest import write_live_manifest

def test_live_playback_dry_run(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    
    manifest_path = tmp_path / "live_manifest.json"
    
    # Create dummy files for playback
    inst0 = tmp_path / "inst_000.wav"
    inst1 = tmp_path / "inst_001.wav"
    inst0.write_text("inst0 data")
    inst1.write_text("inst1 data")
    
    manifest = LiveManifest(
        job_id="live-playback-job",
        youtube_url="https://youtube.com",
        status=LiveStreamStatus.COMPLETED,
        chunk_duration=30.0,
        model_name="htdemucs",
        output_format="wav",
        chunks=[
            LiveChunkMetadata(index=0, status=LiveChunkStatus.READY, start_seconds=0.0, end_seconds=30.0, source_path="s0", instrumental_path=str(inst0)),
            LiveChunkMetadata(index=1, status=LiveChunkStatus.READY, start_seconds=30.0, end_seconds=60.0, source_path="s1", instrumental_path=str(inst1))
        ]
    )
    write_live_manifest(manifest, manifest_path)
    
    options = PlaybackOptions(
        manifest_path=str(manifest_path),
        mode="legacy",
        poll_interval=0.01,
        idle_timeout=1.0
    )
    
    mock_run = MagicMock()
    mock_run.return_value.returncode = 0
    
    with patch("app.services.playback.player.check_ffplay_available", return_value=True), \
         patch("app.services.playback.player.subprocess.run", mock_run):
         
         result = run_playback(options)
         
         assert result.job_id == "live-playback-job"
         assert result.status == "completed"
         assert result.played_chunk_count == 2
         assert result.played_chunk_indices == [0, 1]
         
         # Verify ffplay was called twice
         assert mock_run.call_count == 2
         first_call_args = mock_run.call_args_list[0][0][0]
         second_call_args = mock_run.call_args_list[1][0][0]
         assert "inst_000.wav" in first_call_args[-1]
         assert "inst_001.wav" in second_call_args[-1]
