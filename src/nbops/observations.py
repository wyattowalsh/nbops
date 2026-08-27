"""Observation envelopes and capability status."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class RunState(StrEnum):
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    DEGRADED = "degraded"
    STOPPING = "stopping"
    STOPPED = "stopped"
    STOPPED_WITH_LOSS = "stopped_with_loss"
    FAILED = "failed"
    CLOSED = "closed"


class CapabilityState(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    DISABLED = "disabled"
    UNAVAILABLE = "unavailable"


class ObservationQuality(StrEnum):
    EXACT = "exact"
    ESTIMATED = "estimated"
    STALE = "stale"
    UNAVAILABLE = "unavailable"


class CapabilityStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    state: CapabilityState
    reason: str | None = None


class Observation(BaseModel):
    """Versioned scalar observation. Missing values stay unavailable, never zero."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "nbops.observation.v1"
    run_id: str
    sequence: int = Field(ge=0)
    observed_at_utc: datetime
    monotonic_ns: int
    metric: str
    value_number: float | None = None
    value_text: str | None = None
    unit: str | None = None
    labels: dict[str, str] = Field(default_factory=dict)
    source: str
    quality: ObservationQuality
    collection_duration_ms: float = 0.0

    def value(self) -> float | str | None:
        if self.quality is ObservationQuality.UNAVAILABLE:
            return None
        if self.value_number is not None:
            return self.value_number
        return self.value_text


class ObserverStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str | None
    project: str
    state: RunState
    is_running: bool
    started_at: datetime | None = None
    elapsed_s: float | None = None
    sequence: int = 0
    capabilities: list[CapabilityStatus] = Field(default_factory=list)
    output_dir: str | None = None
    notes: list[str] = Field(default_factory=list)


def new_run_id() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(UTC)


def unavailable(
    *,
    run_id: str,
    sequence: int,
    metric: str,
    source: str,
    unit: str | None = None,
    monotonic_ns: int,
) -> Observation:
    return Observation(
        run_id=run_id,
        sequence=sequence,
        observed_at_utc=utcnow(),
        monotonic_ns=monotonic_ns,
        metric=metric,
        value_number=None,
        value_text=None,
        unit=unit,
        source=source,
        quality=ObservationQuality.UNAVAILABLE,
    )
