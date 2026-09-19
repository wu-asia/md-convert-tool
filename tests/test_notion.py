"""Tests for safe local Notion-export discovery."""

from pathlib import Path

import pytest

from ksync.notion import find_notion_export_files


def test_find_notion_export_files_recurses_for_markdown_and_html(tmp_path: Path) -> None:
    """Only supported document files from an explicit export directory are selected."""
    (tmp_path / "nested").mkdir()
    (tmp_path / "Page.md").write_text("# Page", encoding="utf-8")
    (tmp_path / "nested" / "Database.html").write_text("<p>Page</p>", encoding="utf-8")
    (tmp_path / "asset.png").write_bytes(b"image")

    files = find_notion_export_files(tmp_path)

    assert [path.name for path in files] == ["Database.html", "Page.md"]


def test_find_notion_export_files_rejects_unknown_file_type(tmp_path: Path) -> None:
    """Binary assets are not treated as importable Notion documents."""
    asset = tmp_path / "asset.pdf"
    asset.write_bytes(b"pdf")

    with pytest.raises(ValueError, match="Markdown or HTML"):
        find_notion_export_files(asset)
