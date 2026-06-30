from __future__ import annotations

from threading import Thread
from typing import Any, Callable


def start_background_task(
    target: Callable[..., Any],
    *args: Any,
    name: str | None = None,
) -> Thread:
    """
    Start a daemon thread for background job execution without routing through
    the ASGI threadpool, which can deadlock in some environments.
    """
    thread = Thread(target=target, args=args, name=name, daemon=True)
    thread.start()
    return thread
