"""HTML parsing and primary article selection."""

from __future__ import annotations

from bs4 import BeautifulSoup, Tag


UNWANTED_ELEMENTS = "script, style, nav, footer, header, aside, noscript"


def parse_article(html: str, fallback_title: str) -> tuple[str, str]:
    """Extract title and primary content using article, main, then body fallback."""
    soup = BeautifulSoup(html, "html.parser")
    for element in soup.select(UNWANTED_ELEMENTS):
        element.decompose()

    content = _find_primary_content(soup)
    if content is None or not content.get_text(strip=True):
        raise ValueError("No readable article content was found on this page.")
    return _extract_title(soup, fallback_title), str(content)


def _find_primary_content(soup: BeautifulSoup) -> Tag | None:
    """Return the first supported primary-content element in priority order."""
    for element_name in ("article", "main"):
        content = soup.find(element_name)
        if content is not None:
            return content
    return soup.body


def _extract_title(soup: BeautifulSoup, fallback_title: str) -> str:
    og_title = soup.select_one("meta[property='og:title']")
    if og_title and og_title.get("content"):
        return str(og_title["content"]).strip()
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    heading: Tag | None = soup.find("h1")
    return heading.get_text(" ", strip=True) if heading else fallback_title
