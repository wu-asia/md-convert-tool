# Astro and GitHub Pages Integration

KnowledgeSync writes portable UTF-8 Markdown with YAML Front Matter. Keep the knowledge directory in the same Git repository as an Astro site, or copy/synchronize it into the site's content collection during your build workflow.

## Recommended layout

```text
src/content/notes/
  git-rebase.md
  python-pathlib.md
```

Configure an Astro content collection to validate these fields:

```yaml
title: "Git Rebase"
source: "https://example.com/article"
created: "2026-09-17"
tags:
  - "git"
content_hash: "sha256..."
```

`content_hash` is import metadata and can be omitted from rendered pages. Use `title`, `created`, and `tags` for routes, lists, and tag pages.

## GitHub Pages workflow

1. Run `ksync add ...` or `ksync import-notion ...` locally.
2. Review the generated Markdown and `data/index.json`.
3. Commit the notes and index to Git.
4. Let the existing Astro GitHub Pages workflow build and deploy the site.

KnowledgeSync does not configure, modify, or deploy an Astro project. Site-specific collection schemas, routing, and GitHub Actions remain owned by that project.
