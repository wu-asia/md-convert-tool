"""Tests for safe Markdown note persistence."""

from datetime import datetime, timezone

from ksync.models import KnowledgeNote
from ksync.storage import save_knowledge_note


def test_save_knowledge_note_writes_valid_front_matter_and_prevents_overwrite(tmp_path) -> None:
    """Saved notes include quoted metadata and get a new name when one exists."""
    note = KnowledgeNote(
        title='Git "Rebase"',
        source="https://example.com/article?name=one",
        content="Body text\n",
        created_at=datetime(2026, 9, 17, tzinfo=timezone.utc),
        tags=["git", "version-control"],
        content_hash="abc123",
    )

    first_path = save_knowledge_note(tmp_path, note)
    second_path = save_knowledge_note(tmp_path, note)
    saved = first_path.read_text(encoding="utf-8")

    assert first_path.name == "git-rebase.md"
    assert second_path.name == "git-rebase-2.md"
    assert 'title: "Git \\"Rebase\\""' in saved
    assert 'source: "https://example.com/article?name=one"' in saved
    assert 'created: "2026-09-17"' in saved
    assert '  - "git"' in saved
    assert 'content_hash: "abc123"' in saved
    assert saved.endswith("# Git \"Rebase\"\n\nBody text\n")
