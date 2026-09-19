"""Tests for Markdown whitespace cleanup."""

from ksync.cleaner import clean_markdown


def test_clean_markdown_removes_excess_blank_lines_and_trailing_whitespace() -> None:
    """Prose is normalized while links remain intact."""
    markdown = "# Title   \n\n\n\n[link](https://example.com/a?x=1)   \n"

    cleaned = clean_markdown(markdown)

    assert cleaned == "# Title\n\n[link](https://example.com/a?x=1)\n"


def test_clean_markdown_preserves_fenced_code_content() -> None:
    """Whitespace and blank lines inside a code fence are left unchanged."""
    markdown = "Before\n\n```python\nvalue = 'x'   \n\nprint(value)\n```\n\n\nAfter   \n"

    cleaned = clean_markdown(markdown)

    assert "value = 'x'   \n\nprint(value)" in cleaned
    assert cleaned.endswith("```\n\nAfter\n")
