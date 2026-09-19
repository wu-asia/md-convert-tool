"""Tests for content hashes and the local duplicate index."""

from ksync.deduplicator import content_fingerprint, find_duplicate, load_index, update_index


def test_content_fingerprint_ignores_whitespace_differences() -> None:
    """Line endings, trailing spaces, and repeated whitespace do not change the hash."""
    first = "# Title  \n\nA paragraph\n"
    second = "# Title\r\nA   paragraph   \r\n"

    assert content_fingerprint(first) == content_fingerprint(second)


def test_index_round_trip_and_duplicate_lookup(tmp_path) -> None:
    """An indexed hash can be loaded and resolved to its earlier note metadata."""
    index_path = tmp_path / "index.json"
    entry = {"title": "Git Rebase", "source": "https://example.com", "path": "data/knowledge/git.md"}

    update_index(index_path, "hash-value", entry)

    assert find_duplicate("hash-value", load_index(index_path)) == entry
    assert find_duplicate("missing", load_index(index_path)) is None
