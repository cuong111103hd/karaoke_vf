import sys
import importlib
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_settings_defaults() -> None:
    # Force fresh import/reload of settings module
    if "app.config.settings" in sys.modules:
        importlib.reload(sys.modules["app.config.settings"])
    from app.config.settings import Settings, settings
    
    # Assert defaults
    assert settings.DEMUCS_MODEL_NAME == "htdemucs"
    assert settings.OUTPUT_FORMAT == "wav"
    assert settings.HOST == "127.0.0.1"
    assert settings.PORT == 8000
    
    s = Settings()
    assert s.DEMUCS_MODEL_NAME == "htdemucs"

def test_settings_overrides(monkeypatch) -> None:
    monkeypatch.setenv("DEMUCS_MODEL_NAME", "custom_model")
    monkeypatch.setenv("OUTPUT_FORMAT", "MP3")
    monkeypatch.setenv("PORT", "9000")
    
    # Force reload of settings module so class attributes are re-evaluated
    import app.config.settings
    importlib.reload(app.config.settings)
    
    from app.config.settings import Settings, settings
    assert settings.DEMUCS_MODEL_NAME == "custom_model"
    assert settings.OUTPUT_FORMAT == "mp3"
    assert settings.PORT == 9000
    
    s = Settings()
    assert s.DEMUCS_MODEL_NAME == "custom_model"
    assert s.OUTPUT_FORMAT == "mp3"
    assert s.PORT == 9000
