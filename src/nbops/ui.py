"""Static text/HTML display — the universal correctness path."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from nbops.observations import ObserverStatus


class DisplayResult:
    """Local display payload. No public URL, tunnel, or hosted backend."""

    def __init__(self, *, text: str, html: str) -> None:
        self.text = text
        self.html = html
        self.public_url = None
        self.transport = "static"

    def __str__(self) -> str:
        return self.text


def render_status(
    status: ObserverStatus, observations: list[dict[str, Any]] | None = None
) -> DisplayResult:
    lines = [
        f"nbops [{status.state}] project={status.project} run_id={status.run_id}",
        f"running={status.is_running} sequence={status.sequence}",
    ]
    for capability in status.capabilities:
        reason = f" ({capability.reason})" if capability.reason else ""
        lines.append(f"  {capability.name}: {capability.state.value}{reason}")
    if observations:
        lines.append("observations:")
        for item in observations[-8:]:
            value = item.get("value_number")
            if value is None:
                value = item.get("value_text") or "unavailable"
            lines.append(f"  {item.get('metric')}={value} [{item.get('quality')}]")
    text = "\n".join(lines)
    html = "<pre>" + text.replace("&", "&amp;").replace("<", "&lt;") + "</pre>"
    return DisplayResult(text=text, html=html)


def maybe_ipython_display(result: DisplayResult) -> DisplayResult:
    """Best-effort IPython display; static payload remains the source of truth."""
    try:
        from IPython.display import HTML, display
    except Exception:
        return result
    try:
        display(HTML(result.html))
    except Exception:
        return result
    return result
