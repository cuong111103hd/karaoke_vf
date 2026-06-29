import sys
from pathlib import Path
from unittest.mock import patch

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_demucs_command_construction() -> None:
    from app.integrations.demucs import run_demucs
    
    input_path = Path("/path/to/input.wav")
    output_dir = Path("/path/to/output")
    model = "htdemucs_ft"
    
    with patch("app.integrations.demucs.execute_command") as mock_execute:
        run_demucs(input_path, output_dir, model_name=model)
        
        mock_execute.assert_called_once()
        cmd = mock_execute.call_args[0][0]
        
        # Validate critical command arguments
        assert cmd[0] == sys.executable
        assert cmd[1] == "-m"
        assert cmd[2] == "demucs"
        assert "-n" in cmd
        assert cmd[cmd.index("-n") + 1] == model
        assert "--two-stems=vocals" in cmd
        assert "--jobs" in cmd
        assert cmd[cmd.index("--jobs") + 1] == "1"
        assert "-o" in cmd
        assert cmd[cmd.index("-o") + 1] == str(output_dir)
        assert cmd[-1] == str(input_path)
