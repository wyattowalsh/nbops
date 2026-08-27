"""Observer configuration and output-path preflight."""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from nbops.exceptions import InvalidObserverConfigError, OutputPathError

PrivacyMode = Literal["redacted"]
UiMode = Literal["auto", "static", "text"]


def default_artifact_root() -> Path:
    """Return the platform-appropriate ``nbops`` artifact root."""
    content = Path("/content")
    if content.is_dir():
        return content / "nbops"
    return Path.cwd() / "nbops"


def lexical_normalize(path: Path) -> Path:
    """Normalize ``.`` / ``..`` without requiring the path to exist."""
    raw = os.path.normpath(str(path if path.is_absolute() else Path.cwd() / path))
    return Path(raw)


def is_mounted_drive_target(path: Path) -> bool:
    """Return True when ``path`` lexically resolves under ``/content/drive``."""
    normalized = lexical_normalize(path)
    text = str(normalized)
    return text == "/content/drive" or text.startswith("/content/drive/")


def drive_is_mounted() -> bool:
    """Return True when Google Drive appears mounted at ``/content/drive``."""
    drive = Path("/content/drive")
    try:
        return drive.is_dir() and any(drive.iterdir())
    except OSError:
        return drive.is_dir()


class ObserverConfig(BaseModel):
    """Validated configuration for a local notebook observation run."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    project: str = Field(default="nbops-run", min_length=1, max_length=128)
    output_dir: Path | None = None
    interval_s: float = Field(default=2.0, gt=0)
    collect_gpu: bool = True
    collect_processes: bool = True
    persist: bool = True
    privacy: PrivacyMode = "redacted"
    ui_mode: UiMode = "auto"
    flush_timeout_s: float = Field(default=5.0, gt=0)
    runtime_profile: Literal["auto"] = "auto"
    output_policy: Literal["auto"] = "auto"
    display_transport: Literal["auto"] = "auto"

    @field_validator("interval_s", "flush_timeout_s", mode="before")
    @classmethod
    def _finite_positive(cls, value: Any) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise InvalidObserverConfigError("Timeouts and intervals must be finite numbers.")
        number = float(value)
        if not math.isfinite(number) or number <= 0:
            raise InvalidObserverConfigError("Timeouts and intervals must be finite and positive.")
        return number

    @field_validator("project")
    @classmethod
    def _safe_project(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned or "/" in cleaned or "\\" in cleaned or cleaned in {".", ".."}:
            raise InvalidObserverConfigError("Project names must be a single path-safe token.")
        return cleaned

    def resolved_output_dir(self) -> Path:
        """Return the concrete output directory after defaulting and preflight."""
        target = (
            self.output_dir
            if self.output_dir is not None
            else default_artifact_root() / self.project
        )
        preflight_output_dir(target)
        return lexical_normalize(target)


def preflight_output_dir(path: Path) -> Path:
    """Reject unmounted Drive targets and other unsafe output locations before writes."""
    if is_mounted_drive_target(path) and not drive_is_mounted():
        raise OutputPathError(
            "Configured output path is a mounted-Drive target, but Google Drive is not mounted. "
            "Use a local directory such as /content/nbops/<project> "
            "(or ./nbops/<project> outside Colab)."
        )
    return lexical_normalize(path)


def validate_flush_timeout(value: Any) -> float:
    """Reject boolean, non-finite, or non-positive flush deadlines before waiting."""
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise InvalidObserverConfigError("Flush timeout must be a finite positive number.")
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise InvalidObserverConfigError("Flush timeout must be a finite non-negative number.")
    return number
