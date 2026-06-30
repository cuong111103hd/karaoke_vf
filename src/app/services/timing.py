import time
from typing import Any, Dict, Optional


def record_marker(markers: Dict[str, float], name: str, timestamp: Optional[float] = None) -> float:
    value = time.time() if timestamp is None else timestamp
    markers[name] = value
    return value


def record_duration(
    durations: Dict[str, float],
    name: str,
    started_at: Optional[float],
    finished_at: Optional[float],
) -> None:
    if started_at is None or finished_at is None:
        return
    durations[name] = max(0.0, finished_at - started_at)


def merge_engine_timing(
    markers: Dict[str, float],
    durations: Dict[str, float],
    separation_started_at: Optional[float],
    profile: Optional[Dict[str, Any]],
) -> None:
    if separation_started_at is None or not profile:
        return

    if "subprocess_launch_seconds" in profile:
        inference_started_at = separation_started_at + float(profile.get("subprocess_launch_seconds", 0.0))
        inference_completed_at = inference_started_at + float(profile.get("audio_processing_seconds", 0.0))
        wav_write_started_at = inference_completed_at
        wav_write_completed_at = wav_write_started_at + float(profile.get("wav_finalize_seconds", 0.0))

        markers.setdefault("inference_started_at", inference_started_at)
        markers.setdefault("inference_completed_at", inference_completed_at)
        markers.setdefault("engine_wav_write_started_at", wav_write_started_at)
        markers.setdefault("engine_wav_write_completed_at", wav_write_completed_at)

        durations["engine_launch_seconds"] = float(profile.get("subprocess_launch_seconds", 0.0))
        durations["inference_seconds"] = float(profile.get("audio_processing_seconds", 0.0))
        durations["engine_wav_write_seconds"] = float(profile.get("wav_finalize_seconds", 0.0))
        return

    setup_seconds = float(profile.get("setup_seconds", 0.0))
    inference_started_at = separation_started_at + setup_seconds
    inference_completed_at = inference_started_at + float(profile.get("audio_processing_seconds", 0.0))
    wav_write_started_at = inference_completed_at
    wav_write_completed_at = wav_write_started_at + float(profile.get("wav_finalize_seconds", 0.0))
    cleanup_completed_at = wav_write_completed_at + float(profile.get("cleanup_seconds", 0.0))

    markers.setdefault("inference_started_at", inference_started_at)
    markers.setdefault("inference_completed_at", inference_completed_at)
    markers.setdefault("engine_wav_write_started_at", wav_write_started_at)
    markers.setdefault("engine_wav_write_completed_at", wav_write_completed_at)
    markers.setdefault("engine_cleanup_completed_at", cleanup_completed_at)

    durations["engine_setup_seconds"] = setup_seconds
    durations["inference_seconds"] = float(profile.get("audio_processing_seconds", 0.0))
    durations["engine_wav_write_seconds"] = float(profile.get("wav_finalize_seconds", 0.0))
    durations["engine_cleanup_seconds"] = float(profile.get("cleanup_seconds", 0.0))
