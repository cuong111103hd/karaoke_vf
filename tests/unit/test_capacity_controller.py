import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.capacity_controller import CapacityController, QueueFullError


def _wait_until(predicate, timeout: float = 1.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError("Timed out waiting for condition")


def test_capacity_controller_limits_concurrency_without_blocking_threads() -> None:
    cc = CapacityController(max_concurrent=2, max_queue_size=10)

    events: list[str] = []
    release_job1 = threading.Event()
    release_job2 = threading.Event()
    release_job3 = threading.Event()

    def make_task(job_id: str, release_event: threading.Event):
        def run() -> None:
            events.append(f"{job_id}_executing")
            release_event.wait(timeout=1.0)
            events.append(f"{job_id}_done")
        return run

    cc.submit(
        "job1",
        run=make_task("job1", release_job1),
        on_queued=lambda: events.append("job1_queued"),
        on_running=lambda: events.append("job1_running"),
    )
    cc.submit(
        "job2",
        run=make_task("job2", release_job2),
        on_queued=lambda: events.append("job2_queued"),
        on_running=lambda: events.append("job2_running"),
    )

    _wait_until(lambda: cc.running_count == 2)
    assert cc.queued_count == 0
    assert cc.is_running("job1")
    assert cc.is_running("job2")

    cc.submit(
        "job3",
        run=make_task("job3", release_job3),
        on_queued=lambda: events.append("job3_queued"),
        on_running=lambda: events.append("job3_running"),
    )

    _wait_until(lambda: cc.queued_count == 1)
    assert cc.is_queued("job3")
    assert not cc.is_running("job3")

    release_job1.set()
    _wait_until(lambda: cc.is_running("job3"))
    assert cc.queued_count == 0

    release_job2.set()
    release_job3.set()
    _wait_until(lambda: cc.running_count == 0)

    assert events[:5] == [
        "job1_queued",
        "job2_queued",
        "job1_running",
        "job1_executing",
        "job2_running",
    ]
    assert "job3_queued" in events
    assert "job3_running" in events


def test_capacity_controller_rejects_when_queue_is_full() -> None:
    cc = CapacityController(max_concurrent=1, max_queue_size=1)

    release_job1 = threading.Event()

    cc.submit(
        "job1",
        run=lambda: release_job1.wait(timeout=1.0),
        on_queued=lambda: None,
        on_running=lambda: None,
    )
    _wait_until(lambda: cc.running_count == 1)

    cc.submit(
        "job2",
        run=lambda: None,
        on_queued=lambda: None,
        on_running=lambda: None,
    )
    _wait_until(lambda: cc.queued_count == 1)

    try:
        cc.submit(
            "job3",
            run=lambda: None,
            on_queued=lambda: None,
            on_running=lambda: None,
        )
    except QueueFullError:
        pass
    else:
        raise AssertionError("Expected QueueFullError when queue is full")

    release_job1.set()
    _wait_until(lambda: cc.running_count == 0 and cc.queued_count == 0)
