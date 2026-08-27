---
status: proposed
type: notebook-plan
change: build-colab-observer
tags:
  - colab
  - snippet
  - api
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Colab notebook snippet plan

## Adoption contract

The canonical snippet is generated from source-controlled Python fragments and tested in notebooks and docs. It has three visible cells: install/start, display, and stop/export. Optional Drive mounting is a separate explicit user action, not hidden in the monitor.

## Cell 1 — install, configure, start

Target shape, subject to implementation validation:

```python
%pip install -q "colab-observer[gpu,ui]"

from pathlib import Path
from colab_observer import ObserverConfig, observe

# Safe rerun: flush an observer created by a prior execution of this cell.
_previous = globals().get("observer")
if _previous is not None and _previous.is_running:
    _previous.stop()

config = ObserverConfig(
    project="my-colab-run",
    output_dir=Path("/content/colab-observer/my-colab-run"),
    interval_s=2.0,
    collect_gpu=True,
    collect_processes=True,
    persist=True,
    privacy="redacted",
    ui_mode="auto",
)
observer = observe(config=config)
observer.status()
```

Design notes:

- The documented install extra may change after wheel-size and dependency validation.
- `observe()` returns quickly after initialization.
- Safe rerun stops and flushes the previous run; it does not silently create duplicate samplers.
- Output is local by default.
- `ui_mode="auto"` attempts enhanced local display only through supported/disclosed mechanisms and retains fallback.

## Cell 2 — display

```python
observer.display()
```

Expected behavior:

- Enhanced local widget when available.
- One-time disclosure if current Colab requires enabling its custom widget manager.
- No public URL, tunnel, server process, or share flag.
- Static semantic summary/table fallback on decline/failure.
- Re-running display reuses the active run and does not create another sampler.

## Cell 3 — stop and export

```python
observer.stop()

html_report = observer.export_report(format="html")
markdown_report = observer.export_report(format="markdown")
bundle = observer.export_bundle()

print(f"HTML report: {html_report}")
print(f"Markdown report: {markdown_report}")
print(f"Bundle: {bundle}")
```

Exports return paths even when notebook download UX varies. Partial failures return a structured result or raise a documented exception and do not print a false success path.

## Mounted Drive option

The default quickstart does not authenticate or mount Drive. A separate documentation block may show the official user-driven mount action, followed by:

```python
config = config.model_copy(
    update={"output_dir": Path("/content/drive/MyDrive/colab-observer/my-colab-run")}
)
```

The exact configuration-update API depends on the final config implementation; a dataclass `replace()` path is likely if core avoids Pydantic. Documentation must not show an API that the tested package does not expose.

Before start, the package validates that the chosen directory is writable and identifies mounted-path performance considerations. It does not call a Drive API or move data automatically.

## Optional phase markers

A useful follow-up API:

```python
with observer.phase("training"):
    train()

observer.mark("checkpoint", path="model-step-1000")
```

Marker metadata is bounded and redacted. Phase markers improve diagnostic context but are not required for monitoring.

## Safety invariants

- No `setInterval`, browser clicks, reconnect, activity simulation, audio/video loops, hidden cells, or background requests intended to keep a session alive.
- No automatic accelerator selection or runtime mutation.
- No environment/token output.
- No automatic Drive mount/authentication.
- No remote code download/execution beyond normal reviewed package installation.
- No public dashboard endpoint.

## Snippet source of truth

```text
notebooks/snippets/start.py
notebooks/snippets/display.py
notebooks/snippets/stop_export.py
        │
        ├── generated/validated notebook cells
        ├── docs quickstart code blocks
        └── policy and smoke tests
```

A drift check compares normalized code blocks to source fragments. Notebooks are checked for unexpected outputs, credentials, and prohibited behavior.

## Colab smoke scenarios

1. Clean CPU runtime, local output, static fallback forced.
2. Clean CPU runtime, enhanced widget.
3. NVIDIA runtime with NVML primary.
4. NVIDIA runtime with primary failure and fallback fixture where feasible.
5. Missing optional frameworks.
6. Mounted path unavailable and available.
7. Start-cell rerun, display rerun, stop twice, export twice.
8. Runtime near disk limit, partial export.
9. Widget activation declined.
10. No-network export and report reading.
