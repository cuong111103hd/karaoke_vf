import time
import subprocess
import threading
import logging
import wave
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from app.integrations.youtube import get_youtube_audio_stream_info
from app.services.timing import record_duration, record_marker
from app.services.errors import DownloadError

logger = logging.getLogger(__name__)

class YouTubeStreamingChunkSource:
    def __init__(self, youtube_url: str, job_id: str, initial_buffer_seconds: float = 20.0):
        self.youtube_url = youtube_url
        self.job_id = job_id
        self.initial_buffer_seconds = initial_buffer_seconds
        
        self.metadata: Dict[str, Any] = {}
        self.stream_url: Optional[str] = None
        self.http_headers: Dict[str, str] = {}
        
        self._process: Optional[subprocess.Popen] = None
        self._reader_thread: Optional[threading.Thread] = None
        self._stderr_thread: Optional[threading.Thread] = None
        self._pcm_buffer = bytearray()
        self._stderr_lines = []
        self._lock = threading.RLock()
        self._error: Optional[Exception] = None
        self._is_running = False
        
        # Buffer offset tracking to prevent memory footprint growth
        self._buffer_start_byte = 0
        
        # Inactivity timeout tracking
        self.last_pcm_at = time.time()
        self.chunk_wait_timeout_seconds = 120.0
        self.stream_inactivity_timeout_seconds = 15.0
        
        # Timing storage to pass back to the service
        self.timing_markers: Dict[str, float] = {}
        self.timing_durations: Dict[str, float] = {}
        
        # Audio specs: 44100 Hz, stereo (2 channels), 16-bit (2 bytes) sample width
        self.sample_rate = 44100
        self.channels = 2
        self.sample_width = 2
        self.bytes_per_second = self.sample_rate * self.channels * self.sample_width # 176400
        
        # Record of chunk wait durations: chunk_index -> duration
        self.chunk_wait_durations: Dict[int, float] = {}

    def prepare(self) -> Tuple[Optional[Path], Dict[str, Any], Dict[str, float], Dict[str, float]]:
        """
        Resolves direct URL, metadata, and HTTP headers. Does NOT start the stream.
        """
        start_time = time.time()
        record_marker(self.timing_markers, "stream_info_resolve_started_at", start_time)
        
        try:
            self.stream_url, self.metadata, self.http_headers = get_youtube_audio_stream_info(self.youtube_url)
        except Exception as e:
            raise DownloadError(f"Streaming source stream resolution failed: {str(e)}", original_error=e)
            
        end_time = time.time()
        record_marker(self.timing_markers, "stream_info_resolve_completed_at", end_time)
        record_duration(self.timing_durations, "stream_info_resolve_seconds", start_time, end_time)
        
        return None, self.metadata, self.timing_markers, self.timing_durations

    def start(self) -> None:
        """
        Starts the ffmpeg continuous decoding subprocess and background reader threads.
        """
        if not self.stream_url:
            raise RuntimeError("Streaming source not prepared. Call prepare() first.")
            
        start_time = time.time()
        record_marker(self.timing_markers, "ffmpeg_startup_started_at", start_time)
        self.last_pcm_at = time.time()
        
        # Format HTTP headers for ffmpeg if present
        headers_str = ""
        if self.http_headers:
            headers_list = [f"{k}: {v}" for k, v in self.http_headers.items()]
            headers_str = "\r\n".join(headers_list) + "\r\n"
            
        # Continuous decode command:
        # -y: overwrite
        # -headers: pass http headers to ffmpeg (must come before -i)
        # -i: input stream URL
        # -f s16le: format Signed 16-bit Little Endian PCM
        # -acodec pcm_s16le: PCM audio codec
        # -ar 44100: sample rate 44.1 kHz
        # -ac 2: channels (stereo)
        # pipe:1: output to stdout
        cmd = ["ffmpeg", "-loglevel", "error", "-y"]
        if headers_str:
            cmd.extend(["-headers", headers_str])
        cmd.extend([
            "-i", self.stream_url,
            "-f", "s16le",
            "-acodec", "pcm_s16le",
            "-ar", str(self.sample_rate),
            "-ac", str(self.channels),
            "pipe:1"
        ])
        
        logger.info(
            "Starting ffmpeg streaming decode for job %s (headers=%s)",
            self.job_id,
            "present" if headers_str else "absent",
        )
        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self._is_running = True
            
            # Start background reader threads
            self._reader_thread = threading.Thread(target=self._read_pcm_stream, daemon=True)
            self._reader_thread.start()
            
            self._stderr_thread = threading.Thread(target=self._read_stderr_stream, daemon=True)
            self._stderr_thread.start()
            
        except Exception as e:
            raise DownloadError(f"Failed to start ffmpeg subprocess: {str(e)}", original_error=e)
            
        end_time = time.time()
        record_marker(self.timing_markers, "ffmpeg_startup_completed_at", end_time)
        record_duration(self.timing_durations, "ffmpeg_startup_seconds", start_time, end_time)

    def _read_pcm_stream(self) -> None:
        """
        Background worker that continuously reads PCM bytes from ffmpeg stdout.
        """
        try:
            while self._is_running and self._process:
                # Read PCM in 65KB blocks
                chunk = self._process.stdout.read(65536)
                if not chunk:
                    break
                with self._lock:
                    self._pcm_buffer.extend(chunk)
                    self.last_pcm_at = time.time()
        except Exception as e:
            logger.error(f"Error in background PCM reader thread: {str(e)}")
            self._error = e

    def _read_stderr_stream(self) -> None:
        """
        Background worker that continuously reads stderr to prevent process blocking.
        """
        try:
            while self._is_running and self._process:
                line = self._process.stderr.readline()
                if not line:
                    break
                # Keep last 5 lines
                with self._lock:
                    self._stderr_lines.append(line.decode('utf-8', errors='replace').strip())
                    if len(self._stderr_lines) > 5:
                        self._stderr_lines.pop(0)
        except Exception:
            pass

    def wait_for_chunk(self, index: int, start: float, end: float, output_path: Path) -> None:
        """
        Waits until enough PCM bytes are available in the buffer, extracts the requested window,
        and writes it as a finalized WAV file.
        """
        start_wait_time = time.time()
        
        # Calculate absolute byte positions
        start_byte = int(start * self.bytes_per_second)
        end_byte = int(end * self.bytes_per_second)
        
        # Lock to compute relative byte offsets in the current buffer
        with self._lock:
            relative_start = start_byte - self._buffer_start_byte
            relative_end = end_byte - self._buffer_start_byte
            
        required_bytes = relative_end
        
        logger.info(f"[{self.job_id}] Waiting for chunk {index} source audio ({start:.2f}s - {end:.2f}s, requires {required_bytes} bytes from current buffer)...")
        
        buffer_target_bytes = required_bytes
            
        # Poll the buffer until we have enough bytes or the process exits
        poll_interval = 0.2
        while True:
            with self._lock:
                current_len = len(self._pcm_buffer)
                if self._error:
                    raise DownloadError(f"PCM reader thread failed: {str(self._error)}", original_error=self._error)
                    
            # Check if we met the target
            if current_len >= buffer_target_bytes:
                break
                
            # Check for general chunk wait timeout
            elapsed_wait = time.time() - start_wait_time
            if elapsed_wait > self.chunk_wait_timeout_seconds:
                stderr_msg = " ".join(self._stderr_lines)
                raise DownloadError(f"Timeout waiting for source chunk {index} after {self.chunk_wait_timeout_seconds}s. Stderr: {stderr_msg}")
                
            # Check for inactivity timeout (no bytes read from stream)
            with self._lock:
                inactivity_duration = time.time() - self.last_pcm_at
            if inactivity_duration > self.stream_inactivity_timeout_seconds:
                stderr_msg = " ".join(self._stderr_lines)
                raise DownloadError(
                    f"Stream inactivity timeout: no new audio bytes received for {inactivity_duration:.1f}s (exceeded limit of {self.stream_inactivity_timeout_seconds}s). Stderr: {stderr_msg}"
                )
                
            # Check if ffmpeg subprocess exited early
            if self._process:
                exit_code = self._process.poll()
                if exit_code is not None:
                    # Thread exited, check if we have enough for the minimum requested bytes
                    if current_len >= required_bytes:
                        break
                    # Otherwise, it failed to produce the chunk
                    stderr_msg = " ".join(self._stderr_lines)
                    raise DownloadError(f"ffmpeg exited early with code {exit_code}. Stderr: {stderr_msg}")
                    
            time.sleep(poll_interval)
            
        end_wait_time = time.time()
        wait_duration = end_wait_time - start_wait_time
        self.chunk_wait_durations[index] = wait_duration
        logger.info(f"[{self.job_id}] Chunk {index} source audio ready after waiting {wait_duration:.2f}s")
        
        # Record timing marker for first source chunk ready
        if index == 0:
            record_marker(self.timing_markers, "first_source_chunk_ready_at", end_wait_time)
            
        # Extract the PCM slice
        with self._lock:
            # Safe slice, if the stream ended slightly early, take whatever we have up to relative_end
            pcm_slice = self._pcm_buffer[relative_start:min(relative_end, len(self._pcm_buffer))]
            
        # If the slice is empty, raise an error
        if not pcm_slice:
            raise DownloadError(f"No PCM audio data available for chunk {index} (start={start:.2f}s, end={end:.2f}s)")
            
        # Write WAV file
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with wave.open(str(output_path), "wb") as wav_file:
                wav_file.setnchannels(self.channels)
                wav_file.setsampwidth(self.sample_width)
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(pcm_slice)
        except Exception as e:
            raise DownloadError(f"Failed to write source chunk WAV file: {str(e)}", original_error=e)

    def discard_before(self, seconds: float) -> None:
        """
        Discards PCM buffer bytes corresponding to time before the specified seconds
        to prevent memory footprint from growing indefinitely, while retaining
        necessary overlap.
        """
        discard_byte = int(seconds * self.bytes_per_second)
        with self._lock:
            if discard_byte <= self._buffer_start_byte:
                return
            bytes_to_discard = discard_byte - self._buffer_start_byte
            if bytes_to_discard > len(self._pcm_buffer):
                bytes_to_discard = len(self._pcm_buffer)
            
            # Discard bytes from the beginning of self._pcm_buffer
            del self._pcm_buffer[:bytes_to_discard]
            self._buffer_start_byte = discard_byte
            logger.info(f"[{self.job_id}] Discarded {bytes_to_discard} bytes from PCM buffer. New buffer start byte index: {self._buffer_start_byte} ({seconds:.2f}s)")

    def stop(self) -> None:
        """
        Stops the ffmpeg subprocess and cleans up background threads.
        """
        start_time = time.time()
        record_marker(self.timing_markers, "source_teardown_started_at", start_time)
        
        self._is_running = False
        
        # Terminate ffmpeg process
        if self._process:
            try:
                self._process.terminate()
                self._process.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                logger.warning("ffmpeg process did not terminate. Killing...")
                self._process.kill()
            except Exception as e:
                logger.warning(f"Error terminating ffmpeg process: {str(e)}")
            finally:
                self._process = None
                
        # Join threads
        if self._reader_thread:
            self._reader_thread.join(timeout=1.0)
            self._reader_thread = None
            
        if self._stderr_thread:
            self._stderr_thread.join(timeout=1.0)
            self._stderr_thread = None
            
        end_time = time.time()
        record_marker(self.timing_markers, "source_teardown_completed_at", end_time)
        record_duration(self.timing_durations, "source_teardown_seconds", start_time, end_time)
