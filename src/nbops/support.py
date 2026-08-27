"""Support-tier evaluation from named evidence gates (TASK-113)."""

from __future__ import annotations

from nbops.runtime_profile import RuntimeProfile, SupportEvidence, SupportTier


def evaluate_support(profile: RuntimeProfile, *, representative: bool = False) -> SupportEvidence:
    """Derive a support tier. Local fixtures never promote to validated."""
    if representative:
        return SupportEvidence(
            tier=SupportTier.VALIDATED,
            gates=("representative-runtime",),
            stale=False,
            blocked=False,
        )
    if profile.provider.id == "google-colab":
        return SupportEvidence(
            tier=SupportTier.PREVIEW,
            gates=("local-fixture", "colab-adapter"),
            limitations=("Managed Colab promotion requires representative runtime evidence.",),
        )
    if profile.provider.id == "generic":
        return SupportEvidence(
            tier=SupportTier.UNVERIFIED,
            gates=("generic-python",),
            limitations=("Unknown provider is not host-wide evidence.",),
        )
    return SupportEvidence(
        tier=SupportTier.UNSUPPORTED,
        blocked=True,
        gates=(),
        limitations=("No allowlisted adapter contributed evidence.",),
    )
