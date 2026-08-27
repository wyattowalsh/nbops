"""Passive, bounded, failure-isolated adapter registry (TASK-112)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from nbops.runtime_profile import (
    FacetClaim,
    ProfileConflict,
    generic_python_profile,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from nbops.runtime_profile import RuntimeProfile


@dataclass(frozen=True)
class AdapterContribution:
    name: str
    profile: RuntimeProfile
    failed: bool = False
    error: str | None = None


class AdapterRegistry:
    """Allowlisted adapters contribute evidence; failures stay isolated."""

    def __init__(self) -> None:
        self._adapters: list[tuple[str, Callable[[], RuntimeProfile]]] = []

    def register(self, name: str, probe: Callable[[], RuntimeProfile]) -> None:
        if any(existing == name for existing, _ in self._adapters):
            raise ValueError(f"Adapter already registered: {name}")
        self._adapters.append((name, probe))

    def contribute(self, *, timeout_s: float = 1.0) -> list[AdapterContribution]:
        del timeout_s
        contributions: list[AdapterContribution] = []
        for name, probe in self._adapters:
            try:
                profile = probe()
            except Exception as exc:  # noqa: BLE001 - adapters must not fail the run
                contributions.append(
                    AdapterContribution(
                        name=name,
                        profile=generic_python_profile(colab_signals=False),
                        failed=True,
                        error=type(exc).__name__,
                    )
                )
                continue
            contributions.append(AdapterContribution(name=name, profile=profile))
        return contributions

    def merge(self, contributions: list[AdapterContribution]) -> RuntimeProfile:
        if not contributions:
            return generic_python_profile(colab_signals=False)
        live = [item for item in contributions if not item.failed]
        if not live:
            return generic_python_profile(colab_signals=False)
        base = live[0].profile
        provider_ids = {
            item.profile.provider.id for item in live if item.profile.provider.id != "unknown"
        }
        if len(provider_ids) > 1:
            return base.model_copy(
                update={
                    "provider": FacetClaim(
                        id="unknown",
                        confidence=base.provider.confidence,
                        limitations=("Conflicting provider claims were retained.",),
                    ),
                    "conflicts": (
                        *base.conflicts,
                        ProfileConflict(facet="provider", claims=tuple(sorted(provider_ids))),
                    ),
                }
            )
        return base


def detect_colab_signals() -> bool:
    """Bounded Colab detection from local filesystem/import evidence only."""
    from pathlib import Path

    if Path("/content").is_dir() and Path("/usr/local/bin/colab").exists():
        return True
    try:
        import google.colab  # type: ignore[import-not-found]
    except Exception:
        return Path("/content").is_dir() and "COLAB_RELEASE_TAG" in __import__("os").environ
    return google.colab is not None


def default_registry() -> AdapterRegistry:
    registry = AdapterRegistry()
    registry.register("generic_python", lambda: generic_python_profile(colab_signals=False))
    registry.register(
        "colab",
        lambda: generic_python_profile(colab_signals=detect_colab_signals()),
    )
    return registry
