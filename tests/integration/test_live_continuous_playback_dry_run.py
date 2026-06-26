import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import numpy as np
import soundfile as sf
import pytest

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.playback.service import run_playback
from app.services.playback.models import PlaybackOptions
from app.services.live.models import LiveManifest, LiveChunkMetadata, LiveChunkStatus, LiveStreamStatus
from app.services.live.manifest import write_live_manifest

def test_live_continuous_playback_dry_run(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    
    manifest_path = tmp_path / "live_manifest.json"
    
    # Create valid dummy float32 WAV chunks
    inst0 = tmp_path / "inst_000.wav"
    inst1 = tmp_path / "inst_001.wav"
    
    # 2 seconds chunks at 44100Hz
    data0 = np.ones((88200, 2), dtype=np.float32)
    data1 = np.ones((88200, 2), dtype=np.float32) * 2.0
    
    sf.write(str(inst0), data0, 44100, subtype='FLOAT')
    sf.write(str(inst1), data1, 44100, subtype='FLOAT')
    
    # Create manifest with overlap of 1.0 second
    manifest = LiveManifest(
        job_id="live-playback-continuous-job",
        youtube_url="https://youtube.com",
        status=LiveStreamStatus.COMPLETED,
        chunk_duration=2.0,
        overlap=1.0,
        model_name="htdemucs",
        output_format="wav",
        chunks=[
            LiveChunkMetadata(index=0, status=LiveChunkStatus.READY, start_seconds=0.0, end_seconds=2.0, source_path="s0", instrumental_path=str(inst0)),
            LiveChunkMetadata(index=1, status=LiveChunkStatus.READY, start_seconds=1.0, end_seconds=3.0, source_path="s1", instrumental_path=str(inst1))
        ]
    )
    write_live_manifest(manifest, manifest_path)
    
    options = PlaybackOptions(
        manifest_path=str(manifest_path),
        mode="continuous",
        poll_interval=0.01,
        idle_timeout=1.0
    )
    
    # Run the continuous playback. Since sounddevice is mocked in tests/conftest.py,
    # it won't open a real audio device.
    result = run_playback(options)
    
    assert result.job_id == "live-playback-continuous-job"
    assert result.status == "completed"
    assert result.played_chunk_count == 2
    assert result.played_chunk_indices == [0, 1]
