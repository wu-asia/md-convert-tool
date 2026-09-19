"""Tests for local index search."""

from pathlib import Path

from ksync.search import search_notes


def test_search_notes_matches_stored_markdown_content(tmp_path: Path) -> None:
    """A body-text query returns the indexed note that contains it."""
    note_path = tmp_path / "git.md"
    note_path.write_text("# Git\n\nRebase rewrites commit history.\n", encoding="utf-8")
    index = {
        "hash": {
            "title": "Git Notes",
            "source": "https://example.com/git",
            "path": note_path.as_posix(),
        }
    }

    matches = search_notes("rebase", index)

    assert [entry["title"] for entry in matches] == ["Git Notes"]
