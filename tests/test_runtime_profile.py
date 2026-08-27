"""Runtime profile, adapter registry, and support-tier unit tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from nbops.adapters import AdapterRegistry, default_registry
from nbops.runtime_profile import (
    Confidence,
    FacetClaim,
    ProfileEvidence,
    RuntimeProfile,
    ScopeKind,
    SupportTier,
    generic_python_profile,
)
from nbops.support import evaluate_support


def test_generic_profile_does_not_claim_host_scope() -> None:
    profile = generic_python_profile(colab_signals=False)
    assert profile.provider.id == "generic"
    assert profile.execution_scope is ScopeKind.PROCESS
    assert profile.resource_scope is ScopeKind.UNKNOWN
    assert profile.schema_version.startswith("urn:nbops:")
    dumped = profile.serialize()
    assert dumped["provider"]["id"] == "generic"


def test_colab_signals_do_not_promote_support_without_evidence() -> None:
    profile = generic_python_profile(colab_signals=True)
    support = evaluate_support(profile, representative=False)
    assert support.tier is SupportTier.PREVIEW
    assert support.tier is not SupportTier.VALIDATED


def test_sensitive_evidence_is_redacted() -> None:
    evidence = ProfileEvidence(
        id="env",
        kind="env",
        value="super-secret-token",
        sensitive=True,
        recorded_at=datetime.now(UTC),
    )
    assert evidence.value == "<redacted>"


def test_long_evidence_is_truncated() -> None:
    evidence = ProfileEvidence(
        id="env",
        kind="env",
        value="x" * 300,
        sensitive=False,
        recorded_at=datetime.now(UTC),
    )
    assert evidence.value == "x" * 256


def test_empty_and_all_failed_contributions_use_generic() -> None:
    registry = AdapterRegistry()
    assert registry.merge([]).provider.id == "generic"

    def boom() -> RuntimeProfile:
        raise RuntimeError("nope")

    registry.register("bad", boom)
    merged = registry.merge(registry.contribute())
    assert merged.provider.id == "generic"


def test_detect_colab_signals_without_colab(monkeypatch: pytest.MonkeyPatch) -> None:
    from nbops.adapters import detect_colab_signals

    monkeypatch.setattr("pathlib.Path.is_dir", lambda self: False)
    monkeypatch.setattr("pathlib.Path.exists", lambda self: False)
    assert detect_colab_signals() is False


def test_conflicting_adapters_do_not_pick_a_winner() -> None:
    registry = AdapterRegistry()
    registry.register(
        "a",
        lambda: RuntimeProfile(
            provider=FacetClaim(id="google-colab", confidence=Confidence.CONFIRMED)
        ),
    )
    registry.register(
        "b",
        lambda: RuntimeProfile(provider=FacetClaim(id="deepnote", confidence=Confidence.CONFIRMED)),
    )
    merged = registry.merge(registry.contribute())
    assert merged.provider.id == "unknown"
    assert merged.conflicts
    assert merged.conflicts[0].facet == "provider"


def test_adapter_failure_is_isolated() -> None:
    registry = AdapterRegistry()
    registry.register("ok", lambda: generic_python_profile(colab_signals=False))

    def boom() -> RuntimeProfile:
        raise RuntimeError("adapter exploded")

    registry.register("bad", boom)
    contributions = registry.contribute()
    assert contributions[1].failed is True
    assert contributions[1].error == "RuntimeError"
    merged = registry.merge(contributions)
    assert merged.provider.id == "generic"


def test_default_registry_is_deterministic() -> None:
    first = default_registry().merge(default_registry().contribute())
    second = default_registry().merge(default_registry().contribute())
    assert first.provider.id == second.provider.id
    assert first.display_transports == ("text", "static-html")
