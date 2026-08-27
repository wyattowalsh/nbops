"""Extra observer coverage: fatal sampler, HTML escaping, adapter registry."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from nbops.adapters import AdapterRegistry
from nbops.config import ObserverConfig
from nbops.exports import _escape, export_bundle, export_report
from nbops.observations import CapabilityState, CapabilityStatus, ObserverStatus, RunState
from nbops.observer import Observer
from nbops.runtime_profile import generic_python_profile
from nbops.ui import maybe_ipython_display, render_status


def test_html_escapes_markup(tmp_path: Path) -> None:
    assert (
        _escape('<script>alert("x")</script>')
        == "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;"
    )
    status = ObserverStatus(
        run_id="r",
        project="p",
        state=RunState.STOPPED,
        is_running=False,
        capabilities=[
            CapabilityStatus(name="cpu", state=CapabilityState.AVAILABLE, reason="<b>nope</b>")
        ],
    )
    path = export_report(
        output_dir=tmp_path,
        status=status,
        observations=[
            {
                "metric": "<img>",
                "value_number": None,
                "value_text": "<x>",
                "quality": "unavailable",
                "unit": None,
            }
        ],
        report_format="html",
    )
    text = path.read_text(encoding="utf-8")
    assert "<img>" not in text
    assert "&lt;img&gt;" in text
    assert "&lt;b&gt;nope&lt;/b&gt;" in text
    markdown = export_report(
        output_dir=tmp_path,
        status=status,
        observations=[],
        report_format="markdown",
        profile={"provider": {"id": "generic"}},
    )
    assert "Runtime profile" in markdown.read_text(encoding="utf-8")
    missing = tmp_path / "missing-report.html"
    bundle = export_bundle(
        output_dir=tmp_path,
        status=status,
        sqlite_path=None,
        reports=[missing],
        profile={"provider": {"id": "generic"}},
    )
    assert bundle.is_file()
    assert str(render_status(status))


def test_fatal_sampler_marks_failed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from nbops import sampler as sampler_mod

    def boom(self: object) -> None:
        self._on_fatal("RuntimeError")  # type: ignore[attr-defined]

    monkeypatch.setattr(sampler_mod.Sampler, "_run", boom)
    observer = Observer(
        ObserverConfig(project="fatal", output_dir=tmp_path, persist=False, interval_s=0.05)
    )
    observer.start()
    time.sleep(0.05)
    status = observer.status()
    assert status.state in {RunState.FAILED, RunState.STOPPED_WITH_LOSS, RunState.RUNNING}
    observer.close()


def test_maybe_ipython_display_without_ipython() -> None:
    result = render_status(
        ObserverStatus(run_id="r", project="p", state=RunState.CREATED, is_running=False)
    )
    shown = maybe_ipython_display(result)
    assert shown.text == result.text


def test_duplicate_adapter_register_rejected() -> None:
    registry = AdapterRegistry()
    registry.register("x", lambda: generic_python_profile(colab_signals=False))
    with pytest.raises(ValueError, match="already registered"):
        registry.register("x", lambda: generic_python_profile(colab_signals=False))


def test_evaluate_support_generic_and_unsupported() -> None:
    from nbops.runtime_profile import FacetClaim, RuntimeProfile, SupportTier
    from nbops.support import evaluate_support

    generic = generic_python_profile(colab_signals=False)
    assert evaluate_support(generic).tier is SupportTier.UNVERIFIED
    empty = RuntimeProfile(provider=FacetClaim(id="kaggle"))
    assert evaluate_support(empty).blocked is True
    assert evaluate_support(generic, representative=True).tier is SupportTier.VALIDATED


def test_start_is_idempotent_and_text_ui_skips_ipython(tmp_path: Path) -> None:
    observer = Observer(
        ObserverConfig(
            project="text-ui",
            output_dir=tmp_path,
            persist=False,
            interval_s=0.05,
            ui_mode="text",
        )
    )
    first = observer.start()
    second = observer.start()
    try:
        assert first is second
        assert observer.runtime_profile is not None
        rendered = observer.display()
        assert rendered.public_url is None
        observer.add_note("hello")
        observer.add_phase_marker("train")
        assert any(note.startswith("note:") for note in observer.status().notes)
        markdown = observer.export_report(format="markdown")
        assert markdown.suffix == ".md"
        bundle = observer.export_bundle()
        assert bundle.is_file()
    finally:
        observer.stop()
        observer.close()


def test_export_before_start_creates_output_dir(tmp_path: Path) -> None:
    observer = Observer(
        ObserverConfig(project="export-first", output_dir=tmp_path / "out", persist=False)
    )
    path = observer.export_report(format="html")
    assert path.is_file()
    bundle = observer.export_bundle()
    assert bundle.is_file()


def test_stop_failed_observer_reports_loss(tmp_path: Path) -> None:
    observer = Observer(
        ObserverConfig(project="failed", output_dir=tmp_path, persist=False, interval_s=0.05)
    )
    observer.start()
    observer._on_fatal("boom")
    status = observer.stop(flush_timeout=0.2)
    assert status.state in {RunState.STOPPED_WITH_LOSS, RunState.FAILED}
    observer.close()


def test_start_failure_marks_failed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    observer = Observer(
        ObserverConfig(project="mkdir", output_dir=tmp_path / "blocked", persist=False)
    )

    def boom(self: ObserverConfig) -> Path:
        raise OSError("cannot create output")

    monkeypatch.setattr(ObserverConfig, "resolved_output_dir", boom)
    with pytest.raises(OSError, match="cannot create output"):
        observer.start()
    assert observer.status().state is RunState.FAILED
    observer.close()


def test_maybe_ipython_display_best_effort(monkeypatch: pytest.MonkeyPatch) -> None:
    result = render_status(
        ObserverStatus(run_id="r", project="p", state=RunState.CREATED, is_running=False)
    )
    import sys
    import types

    def html(payload: str) -> str:
        return payload

    def display(payload: str) -> None:
        raise RuntimeError("frontend missing")

    module = types.ModuleType("IPython")
    display_mod = types.ModuleType("IPython.display")
    display_mod.HTML = html
    display_mod.display = display
    monkeypatch.setitem(sys.modules, "IPython", module)
    monkeypatch.setitem(sys.modules, "IPython.display", display_mod)
    shown = maybe_ipython_display(result)
    assert shown.html == result.html
