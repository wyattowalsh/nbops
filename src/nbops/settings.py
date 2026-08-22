"""Environment-backed settings for nbops (``NBOPS_`` prefix)."""

from __future__ import annotations

import sys
from functools import lru_cache

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class NbopsSettings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="NBOPS_", extra="ignore")

    log_level: str = "INFO"
    max_output_chars: int = 100_000
    execute_timeout: int = 120
    progress: bool = True


@lru_cache(maxsize=1)
def get_settings() -> NbopsSettings:
    """Return the process-wide settings singleton."""
    return NbopsSettings()


def configure_logging(level: str | None = None) -> None:
    """Replace the default loguru sink with stderr at ``level``."""
    settings = get_settings()
    logger.remove()
    logger.add(sys.stderr, level=level or settings.log_level)
