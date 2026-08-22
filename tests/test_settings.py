"""Tests for environment-backed settings."""

from __future__ import annotations

import pytest

from nbops.settings import configure_logging, get_settings


@pytest.fixture(autouse=True)
def _clear_settings_cache() -> None:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_settings_defaults() -> None:
    settings = get_settings()
    assert settings.log_level == "INFO"
    assert settings.max_output_chars == 100_000
    assert settings.execute_timeout == 120
    assert settings.progress is True


def test_settings_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NBOPS_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("NBOPS_EXECUTE_TIMEOUT", "30")
    monkeypatch.setenv("NBOPS_PROGRESS", "false")
    get_settings.cache_clear()
    settings = get_settings()
    assert settings.log_level == "DEBUG"
    assert settings.execute_timeout == 30
    assert settings.progress is False


def test_configure_logging_does_not_raise() -> None:
    configure_logging("WARNING")
