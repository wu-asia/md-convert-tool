"""Import helpers for local Markdown and HTML files."""

from __future__ import annotations

import json
from pathlib import Path

from ksync.cleaner import clean_markdown
from ksync.converter import html_to_markdown
from ksync.parser import parse_article


SUPPORTED_SUFFIXES = {".md", ".markdown", ".html", ".htm"}


def read_local_source(path: Path) -> tuple[str, str, str]:
    """Return normalized title, source identifier, and Markdown from a local file."""
    if not path.is_file():
        raise ValueError(f"Local file does not exist: {path}")
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise ValueError("Supported local files are Markdown (.md) and HTML (.html, .htm).")

    text = path.read_text(encoding="utf-8")
    source = path.as_posix()
    if path.suffix.lower() in {".md", ".markdown"}:
        title, markdown = parse_markdown_document(text, path.stem)
        return title, source, clean_markdown(markdown)

    title, article_html = parse_article(text, path.stem)
    return title, source, clean_markdown(html_to_markdown(article_html))


def parse_markdown_document(markdown: str, fallback_title: str) -> tuple[str, str]:
    """Extract a basic quoted ``title`` from Front Matter and preserve the body."""
    body = markdown
    title = fallback_title
    if markdown.startswith("---\n"):
        closing_marker = markdown.find("\n---", 4)
        if closing_marker != -1:
            front_matter = markdown[4:closing_marker]
            body = markdown[closing_marker + 4 :].lstrip("\n")
            for line in front_matter.splitlines():
                if line.startswith("title:"):
                    value = line.removeprefix("title:").strip()
                    try:
                        title = str(json.loads(value))
                    except json.JSONDecodeError:
                        title = value.strip('"') or fallback_title
                    break
    if title == fallback_title:
        for line in body.splitlines():
            if line.startswith("# "):
                title = line[2:].strip() or fallback_title
                break
    return title, body
