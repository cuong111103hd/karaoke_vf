import time
from pathlib import Path
from typing import Generator, Set
from app.services.live.manifest import read_live_manifest
from app.services.live.models import LiveChunkMetadata, LiveChunkStatus, LiveStreamStatus

class ManifestWatcher:
    def __init__(self, manifest_path: Path, poll_interval: float = 1.0, idle_timeout: float = 60.0):
        self.manifest_path = manifest_path
        self.poll_interval = poll_interval
        self.idle_timeout = idle_timeout
        self.played_indices: Set[int] = set()

    def watch(self) -> Generator[LiveChunkMetadata, None, None]:
        """
        Polls the manifest file, yielding ready chunks in order.
        Raises TimeoutError if no new chunks are ready for longer than idle_timeout.
        Raises RuntimeError if the stream status is FAILED.
        """
        last_activity = time.time()
        next_to_play = 0
        
        while True:
            if not self.manifest_path.exists():
                if time.time() - last_activity > self.idle_timeout:
                    raise TimeoutError(f"Manifest file {self.manifest_path} was not created within {self.idle_timeout}s.")
                time.sleep(self.poll_interval)
                continue
                
            try:
                manifest = read_live_manifest(self.manifest_path)
            except Exception:
                # Manifest could be in the middle of an atomic update, or temporarily unreadable
                if time.time() - last_activity > self.idle_timeout:
                    raise TimeoutError(f"Manifest file {self.manifest_path} was unreadable or malformed for {self.idle_timeout}s.")
                time.sleep(self.poll_interval)
                continue
                
            if manifest.status == LiveStreamStatus.FAILED:
                raise RuntimeError(f"Live separation stream failed: {manifest.error_message}")
                
            # Find ready chunks
            ready_chunks = {c.index: c for c in manifest.chunks if c.status == LiveChunkStatus.READY}
            
            yielded_any = False
            while next_to_play in ready_chunks:
                chunk = ready_chunks[next_to_play]
                yield chunk
                self.played_indices.add(next_to_play)
                next_to_play += 1
                last_activity = time.time()
                yielded_any = True
                
            # Check for stream completion
            if manifest.status == LiveStreamStatus.COMPLETED:
                # If all chunks are played, we can finish
                if next_to_play >= len(manifest.chunks):
                    break
                    
            if not yielded_any:
                if time.time() - last_activity > self.idle_timeout:
                    raise TimeoutError(f"No new ready chunks appeared in manifest for {self.idle_timeout}s.")
                    
            time.sleep(self.poll_interval)
