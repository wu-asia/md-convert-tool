"""Safe import discovery for user-provided Notion export directories."""

from __future__ import annotations

from pathlib import Path

from ksync.local_files import SUPPORTED_SUFFIXES


def find_notion_export_files(export_path: Path) -> list[Path]:
    """Return supported files from an explicitly supplied Notion export path.

    This module never authenticates with Notion or accesses remote content.
    """
    if export_path.is_file():
        if export_path.suffix.lower() not in SUPPORTED_SUFFIXES:
            raise ValueError("Notion export file must be Markdown or HTML.")
        return [export_path]
    if not export_path.is_dir():
        raise ValueError(f"Notion export path does not exist: {export_path}")
    return sorted(
        (path for path in export_path.rglob("*") if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES),
        key=lambda path: path.as_posix().casefold(),
    )
