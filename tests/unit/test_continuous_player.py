import pytest
import numpy as np
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.playback.continuous_player import ContinuousPlayer
from app.services.live.models import LiveChunkMetadata, LiveChunkStatus

def test_continuous_player_with_overlap() -> None:
    # Mock queue
    mock_queue = MagicMock()
    mock_queue.manifest_path = Path("/dummy/live_manifest.json")
    
    # 2 ready chunks, then end of stream (None)
    chunk0 = LiveChunkMetadata(
        index=0,
        status=LiveChunkStatus.READY,
        start_seconds=0.0,
        end_seconds=2.0,
        source_path="src0.wav",
        instrumental_path="inst0.wav"
    )
    chunk1 = LiveChunkMetadata(
        index=1,
        status=LiveChunkStatus.READY,
        start_seconds=1.0,
        end_seconds=3.0,
        source_path="src1.wav",
        instrumental_path="inst1.wav"
    )
    mock_queue.get_next_chunk.side_effect = [chunk0, chunk1, None]
    
    # Mock read_live_manifest to return overlap = 1.0 second
    mock_manifest = MagicMock()
    mock_manifest.overlap = 1.0
    
    # Mock load_wav_chunk to return dummy audio
    # samplerate 44100, 2 channels. 2 seconds chunk = 88200 samples.
    dummy_audio0 = np.ones((88200, 2), dtype=np.float32)
    dummy_audio1 = np.ones((88200, 2), dtype=np.float32) * 2.0
    
    def mock_load(path, **kwargs):
        if "inst0" in str(path):
            return dummy_audio0
        return dummy_audio1

    mock_stream_instance = MagicMock()
    
    with patch("app.services.playback.continuous_player.read_live_manifest", return_value=mock_manifest), \
         patch("app.services.playback.continuous_player.load_wav_chunk", side_effect=mock_load), \
         patch("sounddevice.OutputStream", return_value=mock_stream_instance):
         
        player = ContinuousPlayer(mock_queue, samplerate=44100, channels=2)
        player.play()
        
        # Verify stream calls
        mock_stream_instance.start.assert_called_once()
        mock_stream_instance.stop.assert_called_once()
        mock_stream_instance.close.assert_called_once()
        
        # Verify write calls
        assert mock_stream_instance.write.call_count == 3
        
        # Call 1: to_play for chunk 0 (first 44100 samples of ones)
        call1_data = mock_stream_instance.write.call_args_list[0][0][0]
        assert call1_data.shape == (44100, 2)
        assert np.allclose(call1_data, 1.0)
        
        # Call 2: blended overlap (44100 samples)
        call2_data = mock_stream_instance.write.call_args_list[1][0][0]
        assert call2_data.shape == (44100, 2)
        # Check midpoint of blended fade (ones and twos)
        assert np.allclose(call2_data[22050], 1.5, atol=0.01)
        
        # Call 3: pending_tail of chunk 1 at the end (last 44100 samples of twos)
        call3_data = mock_stream_instance.write.call_args_list[2][0][0]
        assert call3_data.shape == (44100, 2)
        assert np.allclose(call3_data, 2.0)
        
        assert player.played_indices == [0, 1]
