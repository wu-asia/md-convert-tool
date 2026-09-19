"""Deterministic Markdown whitespace cleanup."""

from __future__ import annotations

def clean_markdown(markdown: str) -> str:
    """Normalize prose whitespace without changing fenced code-block content."""
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    output: list[str] = []
    in_fence = False
    blank_count = 0
    for line in lines:
        is_fence = line.lstrip().startswith(("```", "~~~"))
        if is_fence:
            in_fence = not in_fence
        normalized_line = line if in_fence or is_fence else line.rstrip()
        if not in_fence and not is_fence and not normalized_line:
            blank_count += 1
            if blank_count > 1:
                continue
        else:
            blank_count = 0
        output.append(normalized_line)
    return "\n".join(output).strip() + "\n"
