"""HTTP retrieval for web sources."""

from __future__ import annotations

import requests

from config.config import REQUEST_TIMEOUT_SECONDS


class FetchError(RuntimeError):
    """Raised when a source page cannot be downloaded."""


HEADERS = {
    "User-Agent": "KnowledgeSync/0.1 (personal knowledge organizer)",
    "Accept": "text/html,application/xhtml+xml",
}


def fetch_html(url: str, timeout: int = REQUEST_TIMEOUT_SECONDS) -> str:
    """Fetch a HTTP(S) URL and return its decoded HTML.

    This function owns only the network request. HTML parsing and persistence
    belong to later pipeline stages.
    """
    if not url.startswith(("https://", "http://")):
        raise FetchError("URL must start with http:// or https://")
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
    except requests.Timeout as error:
        raise FetchError(f"Request timed out while downloading {url}.") from error
    except requests.ConnectionError as error:
        raise FetchError(f"Could not connect to {url}.") from error
    except requests.HTTPError as error:
        raise FetchError(f"Server returned an HTTP error for {url}: {error}") from error
    except requests.RequestException as error:
        raise FetchError(f"Could not download {url}: {error}") from error
    return response.text
