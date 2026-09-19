"""Tests for generic HTML article extraction."""

from pathlib import Path

import pytest

from ksync.parser import parse_article


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "article_page.html"


def test_parse_article_uses_local_fixture_and_removes_non_content_elements() -> None:
    """Article content and document title are selected from a local HTML fixture."""
    html = FIXTURE_PATH.read_text(encoding="utf-8")

    title, article_html = parse_article(html, "https://example.com/fallback")

    assert title == "Test Article"
    assert "Hello KnowledgeSync" in article_html
    assert "KnowledgeSync parser test." in article_html
    assert "This main content must not win" not in article_html
    for unwanted_text in (
        "Site Header",
        "Navigation",
        "Related links",
        "JavaScript is required.",
        "Footer",
    ):
        assert unwanted_text not in article_html


@pytest.mark.parametrize(
    ("html", "expected_content"),
    [
        ("<html><body><main><p>Main fallback</p></main></body></html>", "Main fallback"),
        ("<html><body><p>Body fallback</p></body></html>", "Body fallback"),
    ],
)
def test_parse_article_falls_back_from_article_to_main_to_body(
    html: str, expected_content: str
) -> None:
    """Pages without an article select main, then body as the final fallback."""
    _title, content = parse_article(html, "Fallback title")

    assert expected_content in content


def test_parse_article_uses_fallback_title_when_no_title_or_heading_exists() -> None:
    """The caller-provided fallback is used when the document has no title metadata."""
    title, _content = parse_article("<html><body><p>Content</p></body></html>", "Fallback title")

    assert title == "Fallback title"


def test_parse_article_rejects_pages_without_readable_content() -> None:
    """An empty body produces a clear parsing error."""
    with pytest.raises(ValueError, match="No readable article content"):
        parse_article("<html><body><nav>Only navigation</nav></body></html>", "Fallback")
