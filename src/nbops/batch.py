"""Batch operations over directories of notebooks."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from tqdm import tqdm

from nbops.models import BatchItem

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable


def iter_notebooks(root: str | Path, *, recursive: bool = True) -> list[Path]:
    """Return sorted ``.ipynb`` paths under ``root``, skipping checkpoints."""
    base = Path(root)
    if base.is_file():
        return [base]
    if not base.is_dir():
        return []
    pattern = "**/*.ipynb" if recursive else "*.ipynb"
    paths = [
        path
        for path in base.glob(pattern)
        if path.is_file() and ".ipynb_checkpoints" not in path.parts
    ]
    return sorted(paths)


def map_notebooks[T](
    root: str | Path,
    fn: Callable[[Path], T],
    *,
    recursive: bool = True,
    progress: bool = False,
) -> list[BatchItem[T]]:
    """Apply ``fn`` to every notebook under ``root`` and capture per-file errors."""
    items: list[BatchItem[T]] = []
    paths = iter_notebooks(root, recursive=recursive)
    iterator = tqdm(paths, desc="nbops", unit="nb", disable=not progress)
    for path in iterator:
        try:
            items.append(BatchItem(path=str(path), ok=True, result=fn(path)))
        except Exception as exc:
            items.append(BatchItem(path=str(path), ok=False, error=str(exc)))
    return items


def notebook_paths(paths: Iterable[str | Path]) -> list[Path]:
    """Expand files and directories into a de-duplicated notebook path list."""
    found: list[Path] = []
    seen: set[Path] = set()
    for item in paths:
        for path in iter_notebooks(item):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            found.append(path)
    return found
