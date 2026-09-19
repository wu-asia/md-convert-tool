"""Tests for the web-import CLI orchestration."""

from pathlib import Path

import main as cli


HTML = "<html><head><title>Git Rebase</title></head><body><article><p>Git rebase a branch.</p></article></body></html>"


def test_add_web_article_saves_once_then_reports_duplicate(
    monkeypatch, tmp_path: Path, capsys
) -> None:
    """The CLI runs the pipeline and does not overwrite identical content."""
    monkeypatch.setattr(cli, "KNOWLEDGE_DIRECTORY", tmp_path / "knowledge")
    monkeypatch.setattr(cli, "INDEX_FILE", tmp_path / "index.json")
    monkeypatch.setattr(cli, "fetch_html", lambda _url: HTML)

    assert cli.add_web_article("https://example.com/rebase") == 0
    first_output = capsys.readouterr().out
    assert "Saved:" in first_output
    assert "Tags: git, version-control" in first_output
    assert len(list((tmp_path / "knowledge").glob("*.md"))) == 1

    assert cli.add_web_article("https://example.com/rebase") == 0
    second_output = capsys.readouterr().out
    assert "Duplicate detected" in second_output
    assert len(list((tmp_path / "knowledge").glob("*.md"))) == 1


def test_add_local_file_and_search_command(monkeypatch, tmp_path: Path, capsys) -> None:
    """Local Markdown import becomes visible through the CLI search command."""
    source = tmp_path / "python.md"
    source.write_text("# Python\n\nUse pytest for testing.\n", encoding="utf-8")
    monkeypatch.setattr(cli, "KNOWLEDGE_DIRECTORY", tmp_path / "knowledge")
    monkeypatch.setattr(cli, "INDEX_FILE", tmp_path / "index.json")

    assert cli.add_local_file(source) == 0
    capsys.readouterr()
    assert cli.search_notes_command("pytest") == 0

    assert "Python" in capsys.readouterr().out


def test_import_notion_export_imports_all_supported_local_files(
    monkeypatch, tmp_path: Path, capsys
) -> None:
    """The Notion command imports explicit local export documents without an API."""
    export_directory = tmp_path / "notion-export"
    export_directory.mkdir()
    (export_directory / "Git.md").write_text("# Git\n\nCommit history.\n", encoding="utf-8")
    (export_directory / "ignored.png").write_bytes(b"image")
    monkeypatch.setattr(cli, "KNOWLEDGE_DIRECTORY", tmp_path / "knowledge")
    monkeypatch.setattr(cli, "INDEX_FILE", tmp_path / "index.json")

    assert cli.import_notion_export(export_directory) == 0

    assert "Importing Notion export" in capsys.readouterr().out
    assert len(list((tmp_path / "knowledge").glob("*.md"))) == 1
