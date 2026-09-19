"""Command-line entry point for KnowledgeSync."""

from __future__ import annotations

import argparse
from pathlib import Path

from config.config import INDEX_FILE, KNOWLEDGE_DIRECTORY, PROJECT_ROOT
from ksync.cleaner import clean_markdown
from ksync.converter import html_to_markdown
from ksync.deduplicator import IndexEntry, content_fingerprint, find_duplicate, load_index, update_index
from ksync.fetcher import FetchError, fetch_html
from ksync.local_files import read_local_source
from ksync.models import KnowledgeNote
from ksync.notion import find_notion_export_files
from ksync.parser import parse_article
from ksync.storage import save_knowledge_note
from ksync.search import search_notes
from ksync.tagger import suggest_tags


def build_parser() -> argparse.ArgumentParser:
    """Create the current command-line parser."""
    parser = argparse.ArgumentParser(
        description="KnowledgeSync: organize personal learning material as Markdown."
    )
    parser.add_argument("--version", action="version", version="KnowledgeSync 0.1.0")
    subparsers = parser.add_subparsers(dest="command")
    add_parser = subparsers.add_parser("add", help="Import one URL, Markdown file, or HTML file")
    add_parser.add_argument("source", help="Public HTTP(S) URL or local Markdown/HTML path")
    subparsers.add_parser("list", help="List indexed knowledge notes")
    search_parser = subparsers.add_parser("search", help="Search indexed knowledge notes")
    search_parser.add_argument("query", help="Case-insensitive text to search for")
    notion_parser = subparsers.add_parser(
        "import-notion", help="Import a user-exported Notion Markdown/HTML file or directory"
    )
    notion_parser.add_argument("path", help="Local Notion export file or directory")
    return parser


def main() -> int:
    """Run the available KnowledgeSync commands."""
    arguments = build_parser().parse_args()
    if arguments.command is None:
        print(f"KnowledgeSync project initialized at: {PROJECT_ROOT}")
        return 0
    if arguments.command == "add":
        return add_source(arguments.source)
    if arguments.command == "list":
        return list_notes()
    if arguments.command == "import-notion":
        return import_notion_export(Path(arguments.path))
    return search_notes_command(arguments.query)


def add_source(source: str) -> int:
    """Import one public URL or supported local file."""
    if source.startswith(("https://", "http://")):
        return add_web_article(source)
    return add_local_file(Path(source))


def add_web_article(url: str) -> int:
    """Import one URL through the v0.1 web-to-Markdown pipeline."""
    try:
        print("Fetching...")
        html = fetch_html(url)
        print("Parsing...")
        title, article_html = parse_article(html, url)
        print("Converting...")
        markdown = html_to_markdown(article_html)
        print("Cleaning...")
        content = clean_markdown(markdown)
        return store_note(title, url, content)
    except (FetchError, ValueError, OSError) as error:
        print(f"Error: {error}")
        return 1



def add_local_file(path: Path) -> int:
    """Import one local Markdown or HTML file through the shared storage pipeline."""
    try:
        print("Reading local file...")
        title, source, content = read_local_source(path)
        return store_note(title, source, content)
    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        return 1


def import_notion_export(export_path: Path) -> int:
    """Import supported files from a user-exported Notion file or directory."""
    try:
        files = find_notion_export_files(export_path)
    except ValueError as error:
        print(f"Error: {error}")
        return 1
    if not files:
        print("No Markdown or HTML files found in the Notion export.")
        return 0

    result = 0
    for path in files:
        print(f"Importing Notion export: {path}")
        result = max(result, add_local_file(path))
    return result


def store_note(title: str, source: str, content: str) -> int:
    """Deduplicate, tag, save, and index one normalized Markdown note."""
    try:
        content_hash = content_fingerprint(content)
        print("Checking duplicate...")
        duplicate = find_duplicate(content_hash, load_index(INDEX_FILE))
        if duplicate is not None:
            print("Duplicate detected")
            print(f"Existing file: {duplicate['path']}")
            return 0
        print("Extracting tags...")
        tags = suggest_tags(title, content)
        note = KnowledgeNote(title=title, source=source, content=content, tags=tags, content_hash=content_hash)
        saved_path = save_knowledge_note(KNOWLEDGE_DIRECTORY, note)
        entry: IndexEntry = {"title": title, "source": source, "path": saved_path.as_posix()}
        update_index(INDEX_FILE, content_hash, entry)
    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        return 1
    print("Saved:")
    print(saved_path.as_posix())
    print(f"Tags: {', '.join(tags) if tags else '(none)'}")
    return 0


def list_notes() -> int:
    """Print every indexed note in title order."""
    entries = sorted(load_index(INDEX_FILE).values(), key=lambda entry: entry["title"].casefold())
    if not entries:
        print("No knowledge notes found.")
        return 0
    for entry in entries:
        print(f"{entry['title']} — {entry['path']}")
    return 0


def search_notes_command(query: str) -> int:
    """Print indexed notes matching a title, source, or Markdown-body query."""
    matches = search_notes(query, load_index(INDEX_FILE))
    if not matches:
        print("No matching knowledge notes found.")
        return 0
    for entry in matches:
        print(f"{entry['title']} — {entry['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
