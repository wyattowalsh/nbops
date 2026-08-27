"""ObserverConfig validation and default artifact paths."""

from __future__ import annotations

import math
from pathlib import Path

import pytest
from pydantic import ValidationError

from nbops.config import (
    ObserverConfig,
    default_artifact_root,
    lexical_normalize,
    validate_flush_timeout,
)
from nbops.exceptions import InvalidObserverConfigError


def test_default_artifact_root_ends_with_nbops() -> None:
    assert default_artifact_root().name == "nbops"


def test_kwargs_observe_config(tmp_path: Path) -> None:
    from nbops import observe

    observer = observe(project="kw", output_dir=tmp_path, interval_s=0.05, persist=False)
    try:
        assert observer.config.project == "kw"
        rendered = observer.display()
        assert "kw" in rendered.text or observer.status().project == "kw"
    finally:
        observer.close()


def test_invalid_interval_rejected() -> None:
    with pytest.raises((InvalidObserverConfigError, ValidationError)):
        ObserverConfig(interval_s=0)
    with pytest.raises((InvalidObserverConfigError, ValidationError)):
        ObserverConfig(interval_s=math.inf)
    with pytest.raises((InvalidObserverConfigError, ValidationError)):
        ObserverConfig(project="../escape")
    with pytest.raises((InvalidObserverConfigError, ValidationError)):
        ObserverConfig(interval_s=True)  # type: ignore[arg-type]


def test_drive_mount_helpers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from nbops.config import drive_is_mounted, is_mounted_drive_target

    assert is_mounted_drive_target(Path("/content/drive/MyDrive/nbops"))
    monkeypatch.setattr("nbops.config.Path.is_dir", lambda self: False)
    assert drive_is_mounted() is False


def test_flush_timeout_helper() -> None:
    assert validate_flush_timeout(0) == 0.0
    with pytest.raises(InvalidObserverConfigError):
        validate_flush_timeout(True)
    with pytest.raises(InvalidObserverConfigError):
        validate_flush_timeout("1")  # type: ignore[arg-type]


def test_lexical_normalize_dot_segments(tmp_path: Path) -> None:
    nested = tmp_path / "a" / "." / "b" / ".." / "c"
    normalized = lexical_normalize(nested)
    assert ".." not in normalized.parts
