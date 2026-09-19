"""Tests for HTTP retrieval without real network requests."""

from __future__ import annotations

import pytest
import requests

from ksync import fetcher


class FakeResponse:
    """Minimal response double for fetcher tests."""

    def __init__(self, text: str, error: requests.HTTPError | None = None) -> None:
        self.text = text
        self.error = error

    def raise_for_status(self) -> None:
        """Raise the configured HTTP error, if any."""
        if self.error is not None:
            raise self.error


def test_fetch_html_returns_response_text_and_uses_request_settings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A successful request returns HTML with the configured headers and timeout."""
    received: dict[str, object] = {}

    def fake_get(url: str, **kwargs: object) -> FakeResponse:
        received["url"] = url
        received.update(kwargs)
        return FakeResponse("<html><body>Test</body></html>")

    monkeypatch.setattr(fetcher.requests, "get", fake_get)

    html = fetcher.fetch_html("https://example.com/article", timeout=5)

    assert html == "<html><body>Test</body></html>"
    assert received == {
        "url": "https://example.com/article",
        "headers": fetcher.HEADERS,
        "timeout": 5,
    }


@pytest.mark.parametrize(
    ("request_error", "message"),
    [
        (requests.Timeout("slow response"), "Request timed out"),
        (requests.ConnectionError("offline"), "Could not connect"),
        (requests.HTTPError("404 Client Error"), "Server returned an HTTP error"),
    ],
)
def test_fetch_html_wraps_network_errors(
    monkeypatch: pytest.MonkeyPatch,
    request_error: requests.RequestException,
    message: str,
) -> None:
    """Requests errors are translated into clear domain-specific errors."""
    def fake_get(*_args: object, **_kwargs: object) -> FakeResponse:
        if isinstance(request_error, requests.HTTPError):
            return FakeResponse("", error=request_error)
        raise request_error

    monkeypatch.setattr(fetcher.requests, "get", fake_get)

    with pytest.raises(fetcher.FetchError, match=message):
        fetcher.fetch_html("https://example.com/article")


def test_fetch_html_rejects_non_http_urls() -> None:
    """The fetcher rejects local paths and unsupported URL schemes."""
    with pytest.raises(fetcher.FetchError, match="must start with http"):
        fetcher.fetch_html("file:///tmp/article.html")
