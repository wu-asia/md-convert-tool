# KnowledgeSync

Personal Knowledge Synchronization & Organization Tool.

KnowledgeSync turns public web articles, local Markdown/HTML files, and user-exported Notion files into a Git-friendly Markdown knowledge base.

## Installation

Requires Python 3.11 or newer. Install dependencies from the project root:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Usage

```bash
ksync add https://example.com/article
ksync add ./notes/git.md
ksync add ./exports/article.html
ksync import-notion ./notion-export
ksync list
ksync search rebase
```

Or run without installing the command:

```bash
python main.py add https://example.com/article
```

## Desktop UI

Launch the dependency-free Tkinter interface after installation:

```bash
ksync-ui
```

Paste a public URL, choose a local Markdown/HTML file, or choose a Notion export folder. The output panel shows every conversion step, saved path, tags, or duplicate result.

## Browser UI

For a responsive browser workspace, run:

```bash
ksync-web
```

It opens a local interface at `http://127.0.0.1:8765`. Paste a URL or a local file/export path, review conversion output, and search saved notes from the same page.

## Project Structure

- `config/config.py` centralizes project paths and runtime settings.
- `ksync/` contains import, parsing, conversion, storage, and search modules.
- `data/raw/` stores future raw input material.
- `data/knowledge/` stores future normalized Markdown notes.
- `data/index.json` records exact SHA-256 content hashes for duplicate detection.
- `tests/` contains automated tests.

## Architecture

Source → extraction → Markdown normalization → duplicate detection → tagging → knowledge base.

## Roadmap

1. More robust article extraction and source-specific cleanup rules
2. Enhanced local index and filtering
3. Optional Notion API integration using authorized official access
4. Astro collection customization and publishing automation

## Contributing

Contributions are welcome after the initial public release. Please keep changes focused, typed, and covered by tests.

## License

The license will be selected before the first public release.
