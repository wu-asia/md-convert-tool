"""Simple search over files registered in the local knowledge index."""

from __future__ import annotations

from pathlib import Path

from ksync.deduplicator import IndexEntry


def search_notes(query: str, index: dict[str, IndexEntry]) -> list[IndexEntry]:
    """Return indexed notes whose metadata or stored Markdown contains ``query``."""
    normalized_query = query.casefold().strip()
    if not normalized_query:
        return []
    matches: list[IndexEntry] = []
    for entry in index.values():
        metadata = f"{entry['title']}\n{entry['source']}".casefold()
        content = _read_note(Path(entry["path"]))
        if normalized_query in metadata or normalized_query in content.casefold():
            matches.append(entry)
    return sorted(matches, key=lambda entry: entry["title"].casefold())


def _read_note(path: Path) -> str:
    """Return note content when it remains available; tolerate a stale index entry."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""
