import yt_dlp
from pathlib import Path
from typing import Dict, Any, Tuple
from app.services.errors import DownloadError
from app.storage.paths import get_job_downloads_dir

def download_youtube_audio(youtube_url: str, job_id: str) -> Tuple[Path, Dict[str, Any]]:
    """
    Downloads the audio track of a YouTube video to the job workspace.
    Returns:
        Tuple[Path, Dict[str, Any]]: The path to the raw downloaded file and the metadata dict.
    """
    downloads_dir = get_job_downloads_dir(job_id)
    # Output template forces the filename to start with 'raw' in the downloads folder
    outtmpl = str(downloads_dir / "raw.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            if not info:
                raise DownloadError("Failed to extract video information from YouTube URL.")
            
            # Find the downloaded file path
            downloaded_files = info.get('requested_downloads', [])
            if downloaded_files and len(downloaded_files) > 0:
                raw_path = Path(downloaded_files[0]['filepath'])
            else:
                # Fallback: search for files starting with 'raw.' in downloads_dir
                files = list(downloads_dir.glob("raw.*"))
                if not files:
                    raise DownloadError("yt-dlp ran but no downloaded file was found in the workspace.")
                raw_path = files[0]
                
            metadata = {
                'title': info.get('title'),
                'duration': info.get('duration'),
                'uploader': info.get('uploader'),
                'view_count': info.get('view_count'),
                'webpage_url': info.get('webpage_url'),
            }
            return raw_path, metadata
            
    except Exception as e:
        if isinstance(e, DownloadError):
            raise e
        raise DownloadError(f"Error downloading YouTube URL: {str(e)}", original_error=e)
