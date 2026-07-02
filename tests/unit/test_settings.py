from pathlib import Path

import pytest

from app.config.settings import Settings


SETTING_KEYS = (
    "DATA_DIR",
    "DEMUCS_MODEL_NAME",
    "OUTPUT_FORMAT",
    "PORT",
    "SEPARATION_ENGINE",
    "SEPARATION_MODEL",
    "SEPARATION_MODEL_DIR",
    "MDX_SEGMENT_SIZE",
    "MDX_OVERLAP",
    "MDX_BATCH_SIZE",
    "LIVE_SOURCE_MODE",
)


def clear_setting_environment(monkeypatch) -> None:
    for key in SETTING_KEYS:
        monkeypatch.delenv(key, raising=False)


def test_settings_defaults(monkeypatch, tmp_path) -> None:
    clear_setting_environment(monkeypatch)
    monkeypatch.chdir(tmp_path)

    settings = Settings()

    assert settings.DATA_DIR == tmp_path / "data"
    assert settings.DEMUCS_MODEL_NAME == "htdemucs"
    assert settings.OUTPUT_FORMAT == "wav"
    assert settings.HOST == "127.0.0.1"
    assert settings.PORT == 8000
    assert settings.SEPARATION_ENGINE == "demucs"
    assert settings.SEPARATION_MODEL == ""
    assert settings.SEPARATION_MODEL_DIR == tmp_path / "data" / "models"
    assert settings.MDX_SEGMENT_SIZE == 256
    assert settings.MDX_OVERLAP == 0.25
    assert settings.MDX_BATCH_SIZE == 1
    assert settings.LIVE_SOURCE_MODE == "streaming"


def test_settings_overrides(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("DEMUCS_MODEL_NAME", "custom_model")
    monkeypatch.setenv("OUTPUT_FORMAT", "MP3")
    monkeypatch.setenv("PORT", "9000")
    monkeypatch.setenv("SEPARATION_ENGINE", "mdx_onnx")
    monkeypatch.setenv("SEPARATION_MODEL", "UVR_MDXNET_KARA_2.onnx")
    monkeypatch.setenv("SEPARATION_MODEL_DIR", str(tmp_path / "models"))
    monkeypatch.setenv("MDX_SEGMENT_SIZE", "512")
    monkeypatch.setenv("MDX_OVERLAP", "0.5")
    monkeypatch.setenv("MDX_BATCH_SIZE", "4")
    monkeypatch.setenv("LIVE_SOURCE_MODE", "download")

    settings = Settings()

    assert settings.DEMUCS_MODEL_NAME == "custom_model"
    assert settings.OUTPUT_FORMAT == "mp3"
    assert settings.PORT == 9000
    assert settings.SEPARATION_ENGINE == "mdx_onnx"
    assert settings.SEPARATION_MODEL == "UVR_MDXNET_KARA_2.onnx"
    assert settings.SEPARATION_MODEL_DIR == tmp_path / "models"
    assert settings.MDX_SEGMENT_SIZE == 512
    assert settings.MDX_OVERLAP == 0.5
    assert settings.MDX_BATCH_SIZE == 4
    assert settings.LIVE_SOURCE_MODE == "download"


def test_settings_invalid_engine(monkeypatch) -> None:
    monkeypatch.setenv("SEPARATION_ENGINE", "invalid_engine")
    with pytest.raises(ValueError, match="Invalid SEPARATION_ENGINE"):
        Settings()


def test_settings_invalid_live_source_mode(monkeypatch) -> None:
    monkeypatch.setenv("LIVE_SOURCE_MODE", "invalid_mode")
    with pytest.raises(ValueError, match="Invalid LIVE_SOURCE_MODE"):
        Settings()


@pytest.mark.parametrize(
    ("name", "value", "message"),
    [
        ("MDX_SEGMENT_SIZE", "0", "MDX_SEGMENT_SIZE"),
        ("MDX_OVERLAP", "0", "MDX_OVERLAP"),
        ("MDX_OVERLAP", "1", "MDX_OVERLAP"),
        ("MDX_BATCH_SIZE", "0", "MDX_BATCH_SIZE"),
    ],
)
def test_settings_reject_invalid_mdx_values(monkeypatch, name, value, message) -> None:
    monkeypatch.setenv(name, value)
    with pytest.raises(ValueError, match=message):
        Settings()
