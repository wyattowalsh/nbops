"""Collector, store, and sampler edge coverage."""

from __future__ import annotations

from pathlib import Path

import pytest

from nbops.collectors import (
    CollectionContext,
    collect_cpu,
    collect_gpu,
    collect_memory,
    probe_capabilities,
)
from nbops.observations import ObservationQuality, new_run_id
from nbops.stores import SqliteStore, quality_never_zero


def test_probe_gpu_capability_is_explicit() -> None:
    statuses = probe_capabilities(collect_gpu=True, collect_processes=True)
    names = {item.name: item for item in statuses}
    assert names["cpu"].state.value == "available"
    assert names["gpu"].state.value in {"available", "degraded", "unavailable"}
    disabled = probe_capabilities(collect_gpu=False, collect_processes=False)
    gpu = next(item for item in disabled if item.name == "gpu")
    assert gpu.state.value == "disabled"


def test_gpu_collect_stays_unavailable_without_numeric_zero() -> None:
    observation = collect_gpu(CollectionContext(run_id="r", sequence=1, monotonic_ns=1))
    assert quality_never_zero(observation)
    if observation.quality is ObservationQuality.UNAVAILABLE:
        assert observation.value_number is None


def test_sqlite_roundtrip(tmp_path: Path) -> None:
    store = SqliteStore(tmp_path / "observations.sqlite")
    run_id = new_run_id()
    store.create_run(run_id, "p", "2026-08-26T00:00:00+00:00", "running")
    cpu = collect_cpu(CollectionContext(run_id=run_id, sequence=1, monotonic_ns=1))
    mem = collect_memory(CollectionContext(run_id=run_id, sequence=1, monotonic_ns=1))
    store.append(cpu)
    store.append(mem)
    rows = store.list_observations(run_id)
    assert {row["metric"] for row in rows} >= {cpu.metric, mem.metric}
    store.set_state(run_id, "stopped")
    store.close()
    reopened = SqliteStore(tmp_path / "observations.sqlite")
    assert reopened.list_observations(run_id)
    reopened.close()


def test_quality_never_zero_for_numeric_sample() -> None:
    cpu = collect_cpu(CollectionContext(run_id="r", sequence=1, monotonic_ns=1))
    assert quality_never_zero(cpu)
    if cpu.quality is not ObservationQuality.UNAVAILABLE:
        assert cpu.value() == cpu.value_number


def test_observation_text_value() -> None:
    from datetime import UTC, datetime

    from nbops.observations import Observation

    observation = Observation(
        run_id="r",
        sequence=1,
        observed_at_utc=datetime.now(UTC),
        monotonic_ns=1,
        metric="note",
        value_text="phase",
        source="control",
        quality=ObservationQuality.EXACT,
    )
    assert observation.value() == "phase"


def test_missing_proc_files_are_unavailable(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    missing = tmp_path / "missing"
    monkeypatch.setattr("nbops.collectors.Path", lambda *_args, **_kwargs: missing)
    cpu = collect_cpu(CollectionContext(run_id="r", sequence=1, monotonic_ns=1))
    mem = collect_memory(CollectionContext(run_id="r", sequence=1, monotonic_ns=1))
    assert cpu.quality is ObservationQuality.UNAVAILABLE
    assert mem.quality is ObservationQuality.UNAVAILABLE
