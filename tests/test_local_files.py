"""Tests for local Markdown and HTML imports."""

from pathlib import Path

from ksync.local_files import read_local_source


def test_read_local_markdown_uses_front_matter_title_and_preserves_structure(tmp_path: Path) -> None:
    """Markdown body, table, link, and fenced code are retained after import."""
    source = tmp_path / "paths.md"
    source.write_text(
        '---\ntitle: "Pathlib Notes"\n---\n\n# Pathlib Notes\n\n[docs](https://example.com)\n\n| A | B |\n| - | - |\n| 1 | 2 |\n\n```python\n  print("ok")   \n```\n',
        encoding="utf-8",
    )

    title, _source_name, content = read_local_source(source)

    assert title == "Pathlib Notes"
    assert "[docs](https://example.com)" in content
    assert "| 1 | 2 |" in content
    assert '  print("ok")   ' in content


def test_read_local_html_converts_article_content(tmp_path: Path) -> None:
    """Local HTML uses the same generic parser and Markdown converter as web input."""
    source = tmp_path / "article.html"
    source.write_text(
        "<html><head><title>Local HTML</title></head><body><article><h1>Local HTML</h1><p>Hello.</p></article></body></html>",
        encoding="utf-8",
    )

    title, _source_name, content = read_local_source(source)

    assert title == "Local HTML"
    assert "# Local HTML" in content
    assert "Hello." in content
