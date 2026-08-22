"""Unit tests for typed report models."""

from __future__ import annotations

from nbops.models import OutputRecord, ValidateResponse


def test_output_record_defaults() -> None:
    record = OutputRecord(cell_index=0, output_index=1, output_type="stream")
    assert record.name is None
    assert record.preview is None
    assert record.size == 0


def test_validate_response_invalid() -> None:
    response = ValidateResponse(valid=False, error="bad schema")
    assert response.valid is False
    assert response.error == "bad schema"
