"""Extensible rule-based tag extraction without external services."""

from __future__ import annotations


TAG_RULES: dict[str, tuple[str, ...]] = {
    "git": ("git", "commit", "branch", "merge", "rebase"),
    "version-control": ("git", "commit", "branch", "merge", "rebase"),
    "linux": ("linux", "chmod", "chown", "systemd", "bash"),
    "python": ("python", "pip", "pytest"),
    "algorithm": ("algorithm", "graph", "dynamic programming", "dfs", "bfs"),
    "machine-learning": (
        "machine learning",
        "regression",
        "classification",
        "neural network",
    ),
}


def suggest_tags(title: str, content: str) -> list[str]:
    """Return tags whose configured keywords occur in a note's title or content."""
    searchable_text = f"{title}\n{content}".casefold()
    return [
        tag
        for tag, keywords in TAG_RULES.items()
        if any(keyword.casefold() in searchable_text for keyword in keywords)
    ]
