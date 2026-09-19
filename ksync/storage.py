"""Markdown note storage and YAML front-matter serialization."""

from __future__ import annotations

import json
from pathlib import Path
import re

from ksync.models import KnowledgeNote


def save_knowledge_note(directory: Path, note: KnowledgeNote) -> Path:
    """Create *directory*, serialize *note* as UTF-8 Markdown, and return its path."""
    directory.mkdir(parents=True, exist_ok=True)
    path = unique_path(directory / f"{safe_filename(note.title)}.md")
    path.write_text(render_note(note), encoding="utf-8")
    return path


def build_front_matter(note: KnowledgeNote) -> str:
    """Build the v0.1 front-matter schema."""
    tag_lines = ["tags:"] + [f"  - {json.dumps(tag, ensure_ascii=False)}" for tag in note.tags]
    if not note.tags:
        tag_lines[-1] = "tags: []"
    return "\n".join([
        "---",
        f"title: {json.dumps(note.title, ensure_ascii=False)}",
        f"source: {json.dumps(note.source, ensure_ascii=False)}",
        f"created: {json.dumps(note.created_at.date().isoformat())}",
        *tag_lines,
        f"content_hash: {json.dumps(note.content_hash)}",
        "---",
    ])


def render_note(note: KnowledgeNote) -> str:
    """Render complete Markdown, adding a title heading when the body has none."""
    content = note.content.lstrip()
    if not content.startswith("#"):
        content = f"# {note.title}\n\n{content}"
    return build_front_matter(note) + "\n" + content.rstrip() + "\n"


def safe_filename(title: str) -> str:
    """Produce a portable, readable filename while retaining Unicode letters."""
    cleaned = re.sub(r"[^\w\s-]", "", title.strip().lower(), flags=re.UNICODE)
    cleaned = re.sub(r"[\s_-]+", "-", cleaned).strip("-.")
    return cleaned[:100] or "untitled-note"


def unique_path(path: Path) -> Path:
    """Avoid overwriting a pre-existing note."""
    if not path.exists():
        return path
    for number in range(2, 10_000):
        candidate = path.with_name(f"{path.stem}-{number}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError("Could not find an available output filename.")
