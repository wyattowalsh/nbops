"""Bounded collectors. Missing evidence is unavailable, never silently zero."""

from __future__ import annotations

import shutil
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from nbops.observations import (
    CapabilityState,
    CapabilityStatus,
    Observation,
    ObservationQuality,
    unavailable,
)


@dataclass(frozen=True)
class CollectionContext:
    run_id: str
    sequence: int
    monotonic_ns: int


def probe_capabilities(*, collect_gpu: bool, collect_processes: bool) -> list[CapabilityStatus]:
    capabilities = [
        CapabilityStatus(name="cpu", state=CapabilityState.AVAILABLE, reason=None),
        CapabilityStatus(name="memory", state=CapabilityState.AVAILABLE, reason=None),
        CapabilityStatus(name="persist", state=CapabilityState.AVAILABLE, reason=None),
        CapabilityStatus(name="static_display", state=CapabilityState.AVAILABLE, reason=None),
    ]
    if collect_gpu:
        gpu_reason = _gpu_unavailability_reason()
        capabilities.append(
            CapabilityStatus(
                name="gpu",
                state=CapabilityState.UNAVAILABLE if gpu_reason else CapabilityState.AVAILABLE,
                reason=gpu_reason,
            )
        )
    else:
        capabilities.append(
            CapabilityStatus(name="gpu", state=CapabilityState.DISABLED, reason="collect_gpu=false")
        )
    if collect_processes:
        capabilities.append(
            CapabilityStatus(
                name="processes",
                state=CapabilityState.AVAILABLE,
                reason="Redacted process counts only; command lines are omitted.",
            )
        )
    return capabilities


def _gpu_unavailability_reason() -> str | None:
    if Path("/dev/nvidia0").exists() or shutil.which("nvidia-smi"):
        return None
    return "No NVIDIA device is visible in this runtime."


def collect_cpu(context: CollectionContext) -> Observation:
    percent = _cpu_percent()
    if percent is None:
        return unavailable(
            run_id=context.run_id,
            sequence=context.sequence,
            metric="cpu.percent",
            source="proc",
            unit="percent",
            monotonic_ns=context.monotonic_ns,
        )
    return Observation(
        run_id=context.run_id,
        sequence=context.sequence,
        observed_at_utc=datetime.now(UTC),
        monotonic_ns=context.monotonic_ns,
        metric="cpu.percent",
        value_number=percent,
        unit="percent",
        source="proc",
        quality=ObservationQuality.ESTIMATED,
    )


def collect_memory(context: CollectionContext) -> Observation:
    available = _memory_available_bytes()
    if available is None:
        return unavailable(
            run_id=context.run_id,
            sequence=context.sequence,
            metric="memory.available_bytes",
            source="proc",
            unit="bytes",
            monotonic_ns=context.monotonic_ns,
        )
    return Observation(
        run_id=context.run_id,
        sequence=context.sequence,
        observed_at_utc=datetime.now(UTC),
        monotonic_ns=context.monotonic_ns,
        metric="memory.available_bytes",
        value_number=float(available),
        unit="bytes",
        source="proc",
        quality=ObservationQuality.EXACT,
    )


def collect_gpu(context: CollectionContext) -> Observation:
    reason = _gpu_unavailability_reason()
    observation = unavailable(
        run_id=context.run_id,
        sequence=context.sequence,
        metric="gpu.utilization",
        source="nvml",
        unit="percent",
        monotonic_ns=context.monotonic_ns,
    )
    if reason is None:
        return observation
    return observation


def _cpu_percent() -> float | None:
    first = _read_proc_stat()
    if first is None:
        return None
    time.sleep(0.02)
    second = _read_proc_stat()
    if second is None:
        return None
    idle_delta = second[1] - first[1]
    total_delta = second[0] - first[0]
    if total_delta <= 0:
        return None
    used = 1.0 - (idle_delta / total_delta)
    return max(0.0, min(100.0, used * 100.0))


def _read_proc_stat() -> tuple[int, int] | None:
    path = Path("/proc/stat")
    if not path.is_file():
        return None
    try:
        line = path.read_text(encoding="utf-8").splitlines()[0]
    except OSError:
        return None
    parts = line.split()
    if not parts or parts[0] != "cpu":
        return None
    values = [int(item) for item in parts[1:] if item.isdigit()]
    if len(values) < 4:
        return None
    total = sum(values)
    idle = values[3]
    return total, idle


def _memory_available_bytes() -> int | None:
    path = Path("/proc/meminfo")
    if not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    for line in text.splitlines():
        if line.startswith("MemAvailable:"):
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                return int(parts[1]) * 1024
    return None
