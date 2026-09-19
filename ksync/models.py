"""Domain models shared by the import pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class KnowledgeNote:
    """A source-independent normalized note ready for later pipeline stages."""

    title: str
    source: str
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tags: list[str] = field(default_factory=list)
    content_hash: str = ""
