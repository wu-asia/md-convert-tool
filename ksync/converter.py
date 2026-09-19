"""HTML-to-Markdown conversion."""

from __future__ import annotations

from markdownify import markdownify


def html_to_markdown(html: str) -> str:
    """Convert HTML to Markdown with ATX headings.

    Whitespace normalization is deliberately left to ``clean_markdown`` so the
    two pipeline stages remain independently testable.
    """
    return markdownify(html, heading_style="ATX", bullets="-")
