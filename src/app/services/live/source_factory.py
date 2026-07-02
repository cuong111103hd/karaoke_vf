from typing import Union
from app.services.live.models import LiveOptions
from app.services.live.youtube_source import YouTubeLiveSource
from app.services.live.streaming_source import YouTubeStreamingChunkSource

def get_live_source(
    youtube_url: str,
    job_id: str,
    options: LiveOptions
) -> Union[YouTubeLiveSource, YouTubeStreamingChunkSource]:
    """
    Factory function to select and construct the correct LiveSource implementation.
    """
    if options.source_mode == "streaming":
        return YouTubeStreamingChunkSource(
            youtube_url=youtube_url,
            job_id=job_id,
            initial_buffer_seconds=options.initial_buffer_seconds
        )
    elif options.source_mode == "download":
        return YouTubeLiveSource(
            youtube_url=youtube_url,
            job_id=job_id
        )
    else:
        raise ValueError(f"Unsupported source mode: {options.source_mode}")
