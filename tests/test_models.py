"""Unit tests for typed report models."""

from __future__ import annotations

from nbops.models import AttachmentRecord, NotebookStats, OutputRecord, ValidateResponse


def test_output_record_defaults() -> None:
    record = OutputRecord(cell_index=0, output_index=1, output_type="stream")
    assert record.name is None
    assert record.preview is None
    assert record.size == 0


def test_notebook_stats_empty_cells_description_includes_attachments() -> None:
    description = NotebookStats.model_fields["empty_cells"].description
    assert description is not None
    assert "no attachments" in description
    assert NotebookStats.model_fields["attachment_cells"].default == 0
    assert NotebookStats.model_fields["attachment_files"].default == 0


def test_attachment_record_defaults() -> None:
    record = AttachmentRecord(cell_index=2, filename="plot.png")
    assert record.mime_types == []
    assert record.size == 0


def test_validate_response_invalid() -> None:
    response = ValidateResponse(valid=False, error="bad schema")
    assert response.valid is False
    assert response.error == "bad schema"
