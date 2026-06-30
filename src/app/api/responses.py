from __future__ import annotations

from pathlib import Path
from typing import AsyncIterator, Optional

from fastapi.responses import StreamingResponse


async def _stream_file(path: Path, chunk_size: int = 64 * 1024) -> AsyncIterator[bytes]:
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            yield chunk


def stream_file_response(
    path: Path,
    media_type: str,
    filename: str,
    extra_headers: Optional[dict[str, str]] = None,
) -> StreamingResponse:
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    if extra_headers:
        headers.update(extra_headers)
    return StreamingResponse(
        _stream_file(path),
        media_type=media_type,
        headers=headers,
    )
