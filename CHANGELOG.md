# Changelog

All notable changes to KnowledgeSync are documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-19

### Added

- Web article import through `ksync add URL`.
- HTTP fetching with a User-Agent, timeout, HTTP status validation, and clear request errors.
- Generic HTML parsing that prioritizes `article`, then `main`, then `body`.
- HTML-to-Markdown conversion with ATX headings and Markdown whitespace cleanup.
- A common `KnowledgeNote` data model with source, timestamps, tags, and content hashes.
- UTF-8 Markdown storage with YAML Front Matter and safe, collision-resistant filenames.
- Exact duplicate detection using normalized SHA-256 hashes and `data/index.json`.
- Extensible rule-based tags for Git, Linux, Python, algorithms, and machine learning.
- Local Markdown and HTML import support.
- Local index commands: `ksync list` and `ksync search QUERY`.
- Local import support for user-exported Notion Markdown and HTML files through `ksync import-notion`.
- A Tkinter desktop interface through `ksync-ui`.
- A responsive local browser workspace through `ksync-web`.
- Astro and GitHub Pages integration guidance.
- Automated pytest coverage for the import pipeline, duplicate detection, tagging, storage, CLI, Notion exports, and browser-UI adapter.

### Known limitations

- Article extraction uses generic HTML heuristics; site-specific parsers are not included.
- Duplicate detection is exact-content SHA-256 matching only; semantic similarity is not supported.
- Notion API synchronization, database storage, AI features, and authentication are intentionally out of scope.
- The browser workspace runs locally on `127.0.0.1` and is not a hosted multi-user service.
