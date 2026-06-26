import logging
from pathlib import Path
from typing import Optional, List
import numpy as np

try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
    SOUNDDEVICE_ERROR = None
except (ImportError, OSError) as e:
    sd = None
    SOUNDDEVICE_AVAILABLE = False
    SOUNDDEVICE_ERROR = str(e)

from app.services.playback.audio_queue import AudioQueue
from app.services.playback.chunk_loader import load_wav_chunk
from app.services.playback.crossfade import crossfade_chunks
from app.services.live.manifest import read_live_manifest

logger = logging.getLogger(__name__)

class ContinuousPlayer:
    def __init__(self, queue: AudioQueue, samplerate: int = 44100, channels: int = 2):
        self.queue = queue
        self.samplerate = samplerate
        self.channels = channels
        self.stream = None
        self.pending_tail: Optional[np.ndarray] = None
        self.overlap_samples = 0
        self.played_indices: List[int] = []

    def start(self) -> None:
        """Opens and starts the persistent sounddevice OutputStream."""
        if not SOUNDDEVICE_AVAILABLE or sd is None:
            raise RuntimeError(
                f"Continuous playback is unavailable because sounddevice/PortAudio could not be loaded: {SOUNDDEVICE_ERROR}. "
                "Please install PortAudio (e.g., 'sudo apt-get install libportaudio2') or use '--mode legacy' to use the ffplay fallback."
            )
        logger.info("Starting persistent sounddevice OutputStream...")
        
        # Read manifest to extract overlap metadata
        try:
            manifest = read_live_manifest(self.queue.manifest_path)
            overlap_seconds = manifest.overlap
            self.overlap_samples = int(overlap_seconds * self.samplerate)
            logger.info(f"Overlap config: {overlap_seconds}s ({self.overlap_samples} samples)")
        except Exception as e:
            logger.warning(f"Could not read overlap from manifest, defaulting to 0: {e}")
            self.overlap_samples = 0

        self.stream = sd.OutputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype="float32"
        )
        self.stream.start()
        self.pending_tail = None

    def play(self) -> None:
        """
        Polls chunks from the queue and plays them continuously.
        Handles crossfading for overlapping regions.
        """
        if not self.stream:
            self.start()

        try:
            while True:
                chunk = self.queue.get_next_chunk()
                if chunk is None:
                    # End of stream
                    break

                if len(self.played_indices) == 0:
                    logger.info("[PLAYBACK] Continuous playback has begun.")

                logger.info(f"[PLAYBACK] Playing chunk {chunk.index} ({chunk.start_seconds:.2f}s - {chunk.end_seconds:.2f}s) from {chunk.instrumental_path}")
                if not chunk.instrumental_path:
                    logger.warning(f"Chunk {chunk.index} has no instrumental path, skipping.")
                    continue

                # Load chunk data
                data = load_wav_chunk(
                    Path(chunk.instrumental_path),
                    expected_samplerate=self.samplerate,
                    expected_channels=self.channels
                )

                # Ensure dimensions align for shape checks
                if data.ndim == 1 and self.channels == 2:
                    # Duplicate mono to stereo if needed, though loader should validate channels
                    data = np.stack([data, data], axis=-1)

                # Stitch with pending tail
                if self.overlap_samples > 0:
                    if self.pending_tail is not None:
                        remaining_data = crossfade_chunks(
                            self.pending_tail,
                            data,
                            self.overlap_samples,
                        )
                    else:
                        remaining_data = data

                    # Save new pending tail
                    if len(remaining_data) >= self.overlap_samples:
                        to_play = remaining_data[:-self.overlap_samples]
                        self.pending_tail = remaining_data[-self.overlap_samples:]
                    else:
                        to_play = np.empty((0, self.channels), dtype=np.float32)
                        self.pending_tail = remaining_data

                    if len(to_play) > 0:
                        self.stream.write(to_play)
                else:
                    # No overlap, play directly
                    self.stream.write(data)

                self.played_indices.append(chunk.index)

            # If there's still a pending tail at the end of the stream, write it
            if self.pending_tail is not None and len(self.pending_tail) > 0:
                self.stream.write(self.pending_tail)
                self.pending_tail = None

        finally:
            self.close()

    def close(self) -> None:
        """Stops and closes the stream."""
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                logger.warning(f"Error closing stream: {e}")
            self.stream = None
