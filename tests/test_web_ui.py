"""Tests for the local browser UI's pipeline adapter."""

from pathlib import Path

import web_ui


def test_import_from_browser_captures_existing_pipeline_output(monkeypatch) -> None:
    """Browser imports reuse the existing URL/local import function and its progress."""
    def fake_add_source(source: str) -> int:
        print(f"Imported {source}")
        return 0

    monkeypatch.setattr(web_ui, "add_source", fake_add_source)

    result = web_ui.import_from_browser("https://example.com/article")

    assert result == {"status": 0, "log": "Imported https://example.com/article\n"}


def test_import_from_browser_uses_notion_importer_for_directories(monkeypatch, tmp_path: Path) -> None:
    """A local directory is routed to the explicit Notion-export importer."""
    def fake_notion_import(path: Path) -> int:
        print(f"Notion import: {path.name}")
        return 0

    monkeypatch.setattr(web_ui, "import_notion_export", fake_notion_import)

    result = web_ui.import_from_browser(str(tmp_path))

    assert result["status"] == 0
    assert "Notion import" in str(result["log"])
