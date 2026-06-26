import sys
from unittest.mock import MagicMock

# Mock sounddevice module globally for all pytest runs to bypass PortAudio library requirements
mock_sd = MagicMock()
sys.modules['sounddevice'] = mock_sd
