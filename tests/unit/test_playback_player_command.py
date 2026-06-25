import pytest
import sys
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.playback.player import play_chunk, PlayerError

def test_play_chunk_ffplay_command(tmp_path) -> None:
    dummy_file = tmp_path / "dummy.wav"
    dummy_file.write_text("audio data")
    
    # 1. Test default ffplay command construction
    mock_run = MagicMock()
    mock_run.return_value.returncode = 0
    
    with patch("app.services.playback.player.check_ffplay_available", return_value=True), \
         patch("app.services.playback.player.subprocess.run", mock_run):
         
        play_chunk(dummy_file)
        
        # Check command structure
        mock_run.assert_called_once()
        called_args = mock_run.call_args[0][0]
        assert called_args == ["ffplay", "-nodisp", "-autoexit", str(dummy_file)]

def test_play_chunk_override_command(tmp_path) -> None:
    dummy_file = tmp_path / "dummy.wav"
    dummy_file.write_text("audio data")
    
    # 2. Test command override construction
    mock_run = MagicMock()
    mock_run.return_value.returncode = 0
    
    with patch("app.services.playback.player.subprocess.run", mock_run):
        play_chunk(dummy_file, player_cmd_override="aplay -D default")
        
        mock_run.assert_called_once()
        called_args = mock_run.call_args[0][0]
        assert called_args == ["aplay", "-D", "default", str(dummy_file)]

def test_play_chunk_missing_ffplay(tmp_path) -> None:
    dummy_file = tmp_path / "dummy.wav"
    dummy_file.write_text("audio data")
    
    # 3. Test missing player raises PlayerError
    with patch("app.services.playback.player.check_ffplay_available", return_value=False):
        with pytest.raises(PlayerError, match="ffplay is not installed"):
            play_chunk(dummy_file)
