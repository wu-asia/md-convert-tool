"""Tests for HTML-to-Markdown conversion."""

from ksync.converter import html_to_markdown


def test_html_to_markdown_preserves_common_markdown_structures() -> None:
    """Headings, links, images, lists, quotes, and code convert predictably."""
    html = """
    <h1>Title</h1><h2>Section</h2><p>A <a href="https://example.com">link</a>.</p>
    <img src="image.png" alt="Diagram"><ul><li>One</li><li>Two</li></ul>
    <blockquote><p>Quoted</p></blockquote><p>Use <code>pathlib.Path</code>.</p>
    <pre><code>print("hello")</code></pre>
    """

    markdown = html_to_markdown(html)

    assert "# Title" in markdown
    assert "## Section" in markdown
    assert "[link](https://example.com)" in markdown
    assert "![Diagram](image.png)" in markdown
    assert "* One" in markdown or "- One" in markdown
    assert "> Quoted" in markdown
    assert "`pathlib.Path`" in markdown
    assert 'print("hello")' in markdown
