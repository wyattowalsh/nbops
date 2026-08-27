"""Daemon sampler: isolated collectors, bounded queue, monotonic scheduling."""

from __future__ import annotations

import contextlib
import queue
import threading
import time
from typing import TYPE_CHECKING

from nbops.collectors import CollectionContext, collect_cpu, collect_gpu, collect_memory

if TYPE_CHECKING:
    from collections.abc import Callable

    from nbops.observations import Observation


class Sampler:
    """Background sampler that never monopolizes notebook cell execution."""

    def __init__(
        self,
        *,
        run_id: str,
        interval_s: float,
        collect_gpu: bool,
        on_batch: Callable[[list[Observation]], None],
        on_fatal: Callable[[str], None],
    ) -> None:
        self._run_id = run_id
        self._interval_s = interval_s
        self._collect_gpu = collect_gpu
        self._on_batch = on_batch
        self._on_fatal = on_fatal
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._queue: queue.Queue[list[Observation]] = queue.Queue(maxsize=32)
        self._sequence = 0
        self.lag_events = 0

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, name="nbops-sampler", daemon=True)
        self._thread.start()

    def stop(self, timeout_s: float) -> bool:
        self._stop.set()
        thread = self._thread
        if thread is not None:
            thread.join(timeout=timeout_s)
            return not thread.is_alive()
        return True

    def _run(self) -> None:
        try:
            while not self._stop.is_set():
                started = time.monotonic()
                self._sequence += 1
                context = CollectionContext(
                    run_id=self._run_id,
                    sequence=self._sequence,
                    monotonic_ns=time.monotonic_ns(),
                )
                batch: list[Observation] = []
                for collector in (collect_cpu, collect_memory):
                    try:
                        batch.append(collector(context))
                    except Exception:
                        continue
                if self._collect_gpu:
                    with contextlib.suppress(Exception):
                        batch.append(collect_gpu(context))
                try:
                    self._queue.put_nowait(batch)
                    self._on_batch(batch)
                except queue.Full:
                    self.lag_events += 1
                    with contextlib.suppress(queue.Empty):
                        self._queue.get_nowait()
                    self._on_batch(batch)
                remaining = self._interval_s - (time.monotonic() - started)
                if remaining > 0:
                    self._stop.wait(remaining)
        except Exception as exc:  # noqa: BLE001 - fatal sampler boundary
            self._on_fatal(type(exc).__name__)
