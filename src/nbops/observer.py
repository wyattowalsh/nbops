"""Notebook runtime observer: local-first sampling, persistence, display, and export."""

from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING, Any, Literal

from nbops.adapters import default_registry
from nbops.collectors import probe_capabilities
from nbops.config import ObserverConfig, validate_flush_timeout
from nbops.exceptions import TerminalObserverError
from nbops.exports import export_bundle as write_bundle
from nbops.exports import export_report as write_report
from nbops.observations import (
    Observation,
    ObserverStatus,
    RunState,
    new_run_id,
    utcnow,
)
from nbops.sampler import Sampler
from nbops.stores import SqliteStore
from nbops.ui import DisplayResult, maybe_ipython_display, render_status

if TYPE_CHECKING:
    from pathlib import Path

    from nbops.runtime_profile import RuntimeProfile

_ACTIVE: dict[str, Observer] = {}
_ACTIVE_LOCK = threading.Lock()


class Observer:
    """Inert until ``start()``. Sampling continues independently of notebook cells."""

    def __init__(self, config: ObserverConfig | None = None, **kwargs: Any) -> None:
        self.config = config if config is not None else ObserverConfig(**kwargs)
        self.run_id: str | None = None
        self._state = RunState.CREATED
        self._started_at = None
        self._start_monotonic = 0.0
        self._output_dir: Path | None = None
        self._store: SqliteStore | None = None
        self._sampler: Sampler | None = None
        self._sequence = 0
        self._capabilities = probe_capabilities(
            collect_gpu=self.config.collect_gpu,
            collect_processes=self.config.collect_processes,
        )
        self._notes: list[str] = []
        self._lock = threading.Lock()
        self._profile: RuntimeProfile | None = None
        self._dropped = 0

    @property
    def is_running(self) -> bool:
        return self._state in {RunState.RUNNING, RunState.DEGRADED, RunState.STARTING}

    @property
    def runtime_profile(self) -> RuntimeProfile | None:
        return self._profile

    def start(self) -> Observer:
        with self._lock:
            if self.is_running:
                return self
            self._state = RunState.STARTING
            try:
                self._output_dir = self.config.resolved_output_dir()
                self._output_dir.mkdir(parents=True, exist_ok=True)
                self.run_id = new_run_id()
                self._started_at = utcnow()
                self._start_monotonic = time.monotonic()
                registry = default_registry()
                self._profile = registry.merge(registry.contribute())
                if self.config.persist:
                    self._store = SqliteStore(self._output_dir / "observations.sqlite")
                    self._store.create_run(
                        self.run_id,
                        self.config.project,
                        self._started_at.isoformat(),
                        RunState.RUNNING.value,
                    )
                self._sampler = Sampler(
                    run_id=self.run_id,
                    interval_s=self.config.interval_s,
                    collect_gpu=self.config.collect_gpu,
                    on_batch=self._accept_batch,
                    on_fatal=self._on_fatal,
                )
                self._sampler.start()
                self._state = RunState.RUNNING
            except Exception:
                self._state = RunState.FAILED
                self._close_owned()
                raise
        with _ACTIVE_LOCK:
            if self.run_id:
                _ACTIVE[self.run_id] = self
        return self

    def stop(self, flush_timeout: float | None = None) -> ObserverStatus:
        timeout = validate_flush_timeout(
            self.config.flush_timeout_s if flush_timeout is None else flush_timeout
        )
        with self._lock:
            if self._state in {RunState.STOPPED, RunState.STOPPED_WITH_LOSS, RunState.CLOSED}:
                return self.status()
            if self._state is RunState.FAILED:
                self._state = RunState.STOPPED_WITH_LOSS
                return self.status()
            self._state = RunState.STOPPING
            sampler = self._sampler
        finished = True
        if sampler is not None:
            finished = sampler.stop(timeout)
        with self._lock:
            self._state = RunState.STOPPED if finished else RunState.STOPPED_WITH_LOSS
            if self._store is not None and self.run_id:
                self._store.set_state(self.run_id, self._state.value)
        with _ACTIVE_LOCK:
            if self.run_id:
                _ACTIVE.pop(self.run_id, None)
        return self.status()

    def close(self) -> ObserverStatus:
        if self.is_running:
            self.stop()
        with self._lock:
            self._close_owned()
            if self._state is not RunState.FAILED:
                self._state = RunState.CLOSED
        return self.status()

    def status(self) -> ObserverStatus:
        elapsed = None
        if self._started_at is not None:
            elapsed = time.monotonic() - self._start_monotonic
        return ObserverStatus(
            run_id=self.run_id,
            project=self.config.project,
            state=self._state,
            is_running=self.is_running,
            started_at=self._started_at,
            elapsed_s=elapsed,
            sequence=self._sequence,
            capabilities=list(self._capabilities),
            output_dir=str(self._output_dir) if self._output_dir else None,
            notes=list(self._notes),
        )

    def display(self) -> DisplayResult:
        observations: list[dict[str, Any]] = []
        if self._store is not None and self.run_id:
            observations = self._store.list_observations(self.run_id)
        result = render_status(self.status(), observations)
        if self.config.ui_mode == "text":
            return result
        return maybe_ipython_display(result)

    def export_report(
        self,
        *,
        format: Literal["html", "markdown"] = "markdown",  # noqa: A002
    ) -> Path:
        if self._output_dir is None:
            self._output_dir = self.config.resolved_output_dir()
            self._output_dir.mkdir(parents=True, exist_ok=True)
        observations: list[dict[str, Any]] = []
        if self._store is not None and self.run_id:
            observations = self._store.list_observations(self.run_id)
        profile = self._profile.serialize() if self._profile is not None else None
        return write_report(
            output_dir=self._output_dir,
            status=self.status(),
            observations=observations,
            report_format=format,
            profile=profile,
        )

    def export_bundle(self) -> Path:
        reports = []
        if self._output_dir is not None:
            reports = [path for path in self._output_dir.glob("report.*") if path.is_file()]
        if self._output_dir is None:
            self._output_dir = self.config.resolved_output_dir()
        sqlite_path = None
        if self._store is not None:
            sqlite_path = self._store.path
        profile = self._profile.serialize() if self._profile is not None else None
        return write_bundle(
            output_dir=self._output_dir,
            status=self.status(),
            sqlite_path=sqlite_path,
            reports=reports,
            profile=profile,
        )

    def add_phase_marker(self, label: str) -> None:
        self._control(f"phase:{label}")

    def add_note(self, text: str) -> None:
        self._control(f"note:{text}")

    def _control(self, message: str) -> None:
        if self._state in {
            RunState.STOPPED,
            RunState.STOPPED_WITH_LOSS,
            RunState.FAILED,
            RunState.CLOSED,
            RunState.STOPPING,
        }:
            raise TerminalObserverError(
                "Terminal observer rejected a control event before it entered the sampler queue."
            )
        self._notes.append(message[:256])

    def _accept_batch(self, batch: list[Observation]) -> None:
        with self._lock:
            if not batch:
                return
            self._sequence = batch[-1].sequence
            if self._store is None:
                return
            for observation in batch:
                self._store.append(observation)

    def _on_fatal(self, category: str) -> None:
        with self._lock:
            self._state = RunState.FAILED
            self._notes.append(f"sampler_fatal:{category}")
            if self._store is not None and self.run_id:
                self._store.set_state(self.run_id, self._state.value)

    def _close_owned(self) -> None:
        sampler = self._sampler
        store = self._store
        self._sampler = None
        self._store = None
        if sampler is not None:
            sampler.stop(0.1)
        if store is not None:
            store.close()

    def __enter__(self) -> Observer:
        return self.start()

    def __exit__(self, *exc: object) -> None:
        self.stop()


def observe(config: ObserverConfig | None = None, **kwargs: Any) -> Observer:
    """Construct and start an observer for notebook ergonomics."""
    return Observer(config=config, **kwargs).start()


start_observer = observe
