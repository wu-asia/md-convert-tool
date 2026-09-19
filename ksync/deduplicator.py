"""Exact duplicate detection backed by a JSON content-hash index."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import TypedDict


class IndexEntry(TypedDict):
    """Metadata retained for a previously stored content hash."""

    title: str
    source: str
    path: str


def content_fingerprint(content: str) -> str:
    """Return a stable SHA-256 fingerprint of normalized note content."""
    normalized = " ".join(content.lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def load_index(index_path: Path) -> dict[str, IndexEntry]:
    """Read an existing duplicate index, treating a missing file as empty."""
    if not index_path.exists():
        return {}
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Duplicate index is not valid JSON: {index_path}") from error
    if not isinstance(data, dict):
        raise ValueError(f"Duplicate index must contain a JSON object: {index_path}")
    return data


def find_duplicate(content_hash: str, index: dict[str, IndexEntry]) -> IndexEntry | None:
    """Return the earlier note metadata when an identical hash already exists."""
    return index.get(content_hash)


def update_index(index_path: Path, content_hash: str, entry: IndexEntry) -> None:
    """Record one note in the JSON index using UTF-8 and stable formatting."""
    index = load_index(index_path)
    index[content_hash] = entry
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
