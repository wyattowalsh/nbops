"""TASK-103: freeze observer lifecycle, Colab defaults, and public signatures."""

from __future__ import annotations

import math
import time
from pathlib import Path

import pytest

from nbops import Observer, ObserverConfig, observe, start_observer
from nbops.exceptions import InvalidObserverConfigError, OutputPathError, TerminalObserverError
from nbops.observations import ObservationQuality, RunState, unavailable


def test_observe_is_alias_of_start_observer() -> None:
    assert start_observer is observe


def test_inert_observer_does_not_sample(tmp_path: Path) -> None:
    observer = Observer(ObserverConfig(project="inert", output_dir=tmp_path, persist=False))
    status = observer.status()
    assert status.state is RunState.CREATED
    assert status.is_running is False
    assert observer.run_id is None


def test_start_returns_control_and_stop_is_idempotent(tmp_path: Path) -> None:
    observer = observe(
        ObserverConfig(project="life", output_dir=tmp_path, interval_s=0.05, persist=True)
    )
    try:
        assert observer.is_running is True
        assert observer.run_id
        time.sleep(0.12)
        first = observer.stop()
        second = observer.stop()
        assert first.state in {RunState.STOPPED, RunState.STOPPED_WITH_LOSS}
        assert second.state == first.state
        assert observer.is_running is False
    finally:
        observer.close()


def test_context_manager_stops(tmp_path: Path) -> None:
    with Observer(ObserverConfig(project="cm", output_dir=tmp_path, interval_s=0.05)) as observer:
        assert observer.is_running
    assert observer.status().state in {RunState.STOPPED, RunState.STOPPED_WITH_LOSS}


def test_invalid_flush_timeout_rejected_before_wait(tmp_path: Path) -> None:
    observer = Observer(ObserverConfig(project="flush", output_dir=tmp_path, persist=False))
    observer.start()
    try:
        with pytest.raises(InvalidObserverConfigError):
            observer.stop(flush_timeout=True)  # type: ignore[arg-type]
        with pytest.raises(InvalidObserverConfigError):
            observer.stop(flush_timeout=-1)
        with pytest.raises(InvalidObserverConfigError):
            observer.stop(flush_timeout=math.nan)
    finally:
        observer.stop(flush_timeout=0.2)
        observer.close()


def test_terminal_observer_rejects_control_events(tmp_path: Path) -> None:
    observer = observe(
        ObserverConfig(project="term", output_dir=tmp_path, persist=False, interval_s=0.05)
    )
    observer.stop()
    with pytest.raises(TerminalObserverError, match="Terminal observer rejected"):
        observer.add_note("hello")
    with pytest.raises(TerminalObserverError):
        observer.add_phase_marker("train")


def test_gpu_unavailable_on_cpu_only_runtime(tmp_path: Path) -> None:
    observer = Observer(
        ObserverConfig(project="cpu", output_dir=tmp_path, collect_gpu=True, persist=False)
    )
    gpu = next(item for item in observer.status().capabilities if item.name == "gpu")
    if gpu.state.value == "unavailable":
        assert gpu.reason
        assert "NVIDIA" in gpu.reason or "gpu" in gpu.reason.lower()


def test_unavailable_observation_is_not_zero() -> None:
    observation = unavailable(
        run_id="r",
        sequence=0,
        metric="gpu.utilization",
        source="nvml",
        unit="percent",
        monotonic_ns=1,
    )
    assert observation.quality is ObservationQuality.UNAVAILABLE
    assert observation.value_number is None
    assert observation.value() is None


def test_display_and_exports_are_local(tmp_path: Path) -> None:
    observer = observe(
        ObserverConfig(project="ui", output_dir=tmp_path, interval_s=0.05, ui_mode="static")
    )
    try:
        time.sleep(0.12)
        rendered = observer.display()
        assert rendered.public_url is None
        assert rendered.transport == "static"
        assert "nbops" in rendered.text
        html = observer.export_report(format="html")
        markdown = observer.export_report(format="markdown")
        bundle = observer.export_bundle()
        assert html.is_file() and html.suffix == ".html"
        assert markdown.is_file() and markdown.suffix == ".md"
        assert bundle.is_file() and bundle.suffix == ".zip"
        assert "keepalive" not in html.read_text(encoding="utf-8")
    finally:
        observer.stop()
        observer.close()


def test_unmounted_drive_output_is_rejected(tmp_path: Path) -> None:
    config = ObserverConfig(
        project="drive",
        output_dir=Path("/content/drive/MyDrive/nbops/run"),
        persist=False,
    )
    with pytest.raises(OutputPathError, match="Drive"):
        Observer(config).start()


def test_dot_segment_drive_path_is_rejected() -> None:
    config = ObserverConfig(
        project="drive-dot",
        output_dir=Path("/content/nbops/../drive/MyDrive/run"),
        persist=False,
    )
    with pytest.raises(OutputPathError):
        Observer(config).start()
