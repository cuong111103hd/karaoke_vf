import time
from pathlib import Path
from typing import Optional
from app.services.live.manifest import read_live_manifest
from app.services.live.models import LiveChunkMetadata, LiveChunkStatus, LiveStreamStatus

class AudioQueue:
    def __init__(self, manifest_path: Path, min_ready_chunks: int = 1, poll_interval: float = 1.0, idle_timeout: float = 60.0):
        self.manifest_path = manifest_path
        self.min_ready_chunks = min_ready_chunks
        self.poll_interval = poll_interval
        self.idle_timeout = idle_timeout
        self.next_index = 0
        self.started = False

    def get_next_chunk(self) -> Optional[LiveChunkMetadata]:
        """
        Retrieves the next ready chunk in order.
        Waits/polls if it is not yet ready.
        Returns None when the stream is completed and all chunks are played.
        Raises TimeoutError if no new chunks are ready for longer than idle_timeout.
        Raises RuntimeError if the stream is failed.
        """
        last_activity = time.time()
        
        while True:
            if not self.manifest_path.exists():
                if time.time() - last_activity > self.idle_timeout:
                    raise TimeoutError(f"Manifest file {self.manifest_path} was not created within {self.idle_timeout}s.")
                time.sleep(self.poll_interval)
                continue
                
            try:
                manifest = read_live_manifest(self.manifest_path)
            except Exception:
                if time.time() - last_activity > self.idle_timeout:
                    raise TimeoutError(f"Manifest file {self.manifest_path} was unreadable or malformed for {self.idle_timeout}s.")
                time.sleep(self.poll_interval)
                continue
                
            ready_chunks = {c.index: c for c in manifest.chunks if c.status == LiveChunkStatus.READY}
            
            # 1. Startup buffering check
            if not self.started:
                is_completed_or_failed = manifest.status in (LiveStreamStatus.COMPLETED, LiveStreamStatus.FAILED)
                if len(ready_chunks) >= self.min_ready_chunks or is_completed_or_failed:
                    self.started = True
                else:
                    if time.time() - last_activity > self.idle_timeout:
                        raise TimeoutError(f"Startup buffering failed: only {len(ready_chunks)}/{self.min_ready_chunks} chunks ready in {self.idle_timeout}s.")
                    time.sleep(self.poll_interval)
                    continue
            
            # 2. Check next chunk index
            if self.next_index in ready_chunks:
                chunk = ready_chunks[self.next_index]
                self.next_index += 1
                return chunk
                
            # If next chunk is not ready, check if stream is failed
            if manifest.status == LiveStreamStatus.FAILED:
                failed_chunk = next((c for c in manifest.chunks if c.index == self.next_index), None)
                err_msg = failed_chunk.error_message if failed_chunk else manifest.error_message
                raise RuntimeError(f"Live separation stream failed at chunk {self.next_index}: {err_msg}")
                
            # Check if stream is completed
            if manifest.status == LiveStreamStatus.COMPLETED:
                if self.next_index >= len(manifest.chunks):
                    return None
                    
            if time.time() - last_activity > self.idle_timeout:
                raise TimeoutError(f"No new ready chunk at index {self.next_index} in manifest for {self.idle_timeout}s.")
                
            time.sleep(self.poll_interval)
