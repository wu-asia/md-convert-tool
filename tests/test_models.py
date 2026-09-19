"""Tests for the common knowledge-note model."""

from datetime import datetime, timezone

from ksync.models import KnowledgeNote


def test_knowledge_note_keeps_shared_metadata() -> None:
    """Every input source can be represented by the same note model."""
    created_at = datetime(2026, 9, 17, tzinfo=timezone.utc)
    note = KnowledgeNote(
        title="Python Paths",
        source="https://example.com/paths",
        content="# Python Paths\n",
        created_at=created_at,
        tags=["python"],
        content_hash="abc123",
    )

    assert note.created_at == created_at
    assert note.tags == ["python"]
    assert note.content_hash == "abc123"
