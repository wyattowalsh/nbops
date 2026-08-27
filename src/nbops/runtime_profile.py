"""Faceted runtime profile models (TASK-110)."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Confidence(StrEnum):
    CONFIRMED = "confirmed"
    PROBABLE = "probable"
    WEAK = "weak"
    UNKNOWN = "unknown"


class SupportTier(StrEnum):
    VALIDATED = "validated"
    PREVIEW = "preview"
    EXPERIMENTAL = "experimental"
    UNVERIFIED = "unverified"
    UNSUPPORTED = "unsupported"


class ScopeKind(StrEnum):
    KERNEL = "kernel"
    PROCESS = "process"
    CONTAINER = "container"
    SERVER = "server"
    HOST = "host"
    UNKNOWN = "unknown"


class FacetClaim(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = "unknown"
    release: str | None = None
    confidence: Confidence = Confidence.UNKNOWN
    evidence_ids: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()


class ProfileEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    kind: str
    value: str
    sensitive: bool = False
    recorded_at: datetime

    @model_validator(mode="after")
    def _redact_sensitive(self) -> ProfileEvidence:
        if self.sensitive:
            self.value = "<redacted>"
        elif len(self.value) > 256:
            self.value = self.value[:256]
        return self


class ProfileConflict(BaseModel):
    model_config = ConfigDict(extra="forbid")

    facet: str
    claims: tuple[str, ...]
    resolution: Literal["unresolved"] = "unresolved"


class SupportEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tier: SupportTier = SupportTier.UNVERIFIED
    stale: bool = False
    blocked: bool = False
    gates: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()


class KernelProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    language: str = "python"
    implementation: str | None = None
    version: str | None = None
    confidence: Confidence = Confidence.PROBABLE


class RuntimeProfile(BaseModel):
    """Versioned faceted runtime identity. Unknown facets stay unknown."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "urn:nbops:runtime-profile:v1"
    provider: FacetClaim = Field(default_factory=FacetClaim)
    frontend: FacetClaim = Field(default_factory=FacetClaim)
    kernel: KernelProfile = Field(default_factory=KernelProfile)
    execution_scope: ScopeKind = ScopeKind.PROCESS
    resource_scope: ScopeKind = ScopeKind.UNKNOWN
    limit_sources: tuple[str, ...] = ()
    storage_locations: tuple[str, ...] = ()
    display_transports: tuple[str, ...] = ("text", "static-html")
    capabilities: tuple[str, ...] = ()
    support: SupportEvidence = Field(default_factory=SupportEvidence)
    evidence: tuple[ProfileEvidence, ...] = ()
    conflicts: tuple[ProfileConflict, ...] = ()
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def serialize(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def generic_python_profile(*, colab_signals: bool) -> RuntimeProfile:
    """Build a truthful generic or Colab-flagged profile without inferring host scope."""
    provider = FacetClaim(
        id="google-colab" if colab_signals else "generic",
        confidence=Confidence.PROBABLE if colab_signals else Confidence.UNKNOWN,
        limitations=()
        if colab_signals
        else ("No recognized notebook provider; kernel-local evidence only.",),
    )
    frontend = FacetClaim(
        id="google-colab" if colab_signals else "unknown",
        confidence=Confidence.PROBABLE if colab_signals else Confidence.UNKNOWN,
        limitations=("Frontend identity is independent of kernel language.",),
    )
    return RuntimeProfile(
        provider=provider,
        frontend=frontend,
        kernel=KernelProfile(language="python", implementation="cpython"),
        execution_scope=ScopeKind.PROCESS,
        resource_scope=ScopeKind.CONTAINER if colab_signals else ScopeKind.UNKNOWN,
        limit_sources=("unknown",),
        storage_locations=("/content/nbops",) if colab_signals else ("nbops",),
        support=SupportEvidence(
            tier=SupportTier.PREVIEW if colab_signals else SupportTier.UNVERIFIED,
            gates=("local-fixture",),
            limitations=("Managed-runtime claims require representative evidence.",),
        ),
    )
