"""Tests for rule-based tagging."""

from ksync.tagger import suggest_tags


def test_suggest_tags_uses_title_and_content_keywords() -> None:
    """Matched category rules are returned in their configured order."""
    tags = suggest_tags("Git workflow", "Use rebase before merging a branch.")

    assert tags == ["git", "version-control"]


def test_suggest_tags_returns_empty_list_when_no_rule_matches() -> None:
    """Unmatched content is allowed and receives no guessed tag."""
    assert suggest_tags("Cooking", "A recipe for bread.") == []
