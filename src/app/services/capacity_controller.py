import logging
import threading
from dataclasses import dataclass
from queue import Queue
from threading import Thread
from typing import Callable, Set
from app.config.settings import settings

logger = logging.getLogger(__name__)

class QueueFullError(RuntimeError):
    """Raised when the in-process separation queue is full."""


@dataclass
class QueuedSeparationTask:
    job_id: str
    run: Callable[[], None]
    on_queued: Callable[[], None]
    on_running: Callable[[], None]


class CapacityController:
    def __init__(self, max_concurrent: int, max_queue_size: int | None = None) -> None:
        self.max_concurrent = max_concurrent
        self.max_queue_size = max_queue_size or settings.MAX_QUEUE_SIZE
        self._lock = threading.RLock()
        self._task_queue: Queue[QueuedSeparationTask] = Queue()
        self._queued_jobs: Set[str] = set()
        self._running_jobs: Set[str] = set()
        self._workers_started = False

    def submit(
        self,
        job_id: str,
        run: Callable[[], None],
        on_queued: Callable[[], None],
        on_running: Callable[[], None],
    ) -> None:
        """
        Enqueue a heavy separation task for execution on the shared worker pool.

        This is a true in-process queue: accepted jobs wait in the queue without
        creating one blocked thread per job.
        """
        self._ensure_workers_started()

        with self._lock:
            if len(self._queued_jobs) >= self.max_queue_size:
                raise QueueFullError("Separation queue is full.")
            self._queued_jobs.add(job_id)

        on_queued()
        self._task_queue.put(
            QueuedSeparationTask(
                job_id=job_id,
                run=run,
                on_queued=on_queued,
                on_running=on_running,
            )
        )
        logger.info(
            "Job %s accepted into capacity queue (active=%s, queued=%s)",
            job_id,
            self.running_count,
            self.queued_count,
        )

    def _ensure_workers_started(self) -> None:
        with self._lock:
            if self._workers_started:
                return
            self._workers_started = True

            for index in range(self.max_concurrent):
                worker = Thread(
                    target=self._worker_loop,
                    name=f"separation-worker-{index}",
                    daemon=True,
                )
                worker.start()

    def _worker_loop(self) -> None:
        while True:
            task = self._task_queue.get()
            try:
                with self._lock:
                    self._queued_jobs.discard(task.job_id)
                    self._running_jobs.add(task.job_id)

                task.on_running()
                logger.info(
                    "Job %s started from capacity queue (active=%s, queued=%s)",
                    task.job_id,
                    self.running_count,
                    self.queued_count,
                )
                task.run()
            except Exception:
                logger.exception("Queued separation task %s crashed", task.job_id)
            finally:
                with self._lock:
                    self._running_jobs.discard(task.job_id)
                logger.info(
                    "Job %s finished capacity slot (active=%s, queued=%s)",
                    task.job_id,
                    self.running_count,
                    self.queued_count,
                )
                self._task_queue.task_done()

    @property
    def queued_count(self) -> int:
        with self._lock:
            return len(self._queued_jobs)

    @property
    def running_count(self) -> int:
        with self._lock:
            return len(self._running_jobs)
            
    def is_queued(self, job_id: str) -> bool:
        with self._lock:
            return job_id in self._queued_jobs

    def is_running(self, job_id: str) -> bool:
        with self._lock:
            return job_id in self._running_jobs


# Global singleton instance
capacity_controller = CapacityController(
    max_concurrent=settings.MAX_CONCURRENT_SEPARATION_JOBS,
    max_queue_size=settings.MAX_QUEUE_SIZE,
)
