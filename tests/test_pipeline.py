from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ksync.converter import html_to_markdown
from ksync.models import KnowledgeNote
from ksync.parser import parse_article
from ksync.storage import safe_filename, save_knowledge_note


HTML = """
<html><head><title>Example Article</title></head><body>
<nav>Navigation</nav><article><h1>Example Article</h1><p>Hello <strong>world</strong>.</p><ul><li>One</li></ul></article>
</body></html>
"""


class PipelineTests(unittest.TestCase):
    def test_article_to_markdown_and_note(self) -> None:
        title, article = parse_article(HTML, "https://example.com")
        markdown = html_to_markdown(article)

        with TemporaryDirectory() as temp_directory:
            note = KnowledgeNote(title, "https://example.com", markdown)
            output = save_knowledge_note(Path(temp_directory), note)
            self.assertEqual(output.name, "example-article.md")
            saved = output.read_text(encoding="utf-8")

        self.assertIn('title: "Example Article"', saved)
        self.assertIn("Hello **world**.", saved)
        self.assertNotIn("Navigation", saved)

    def test_slugify_preserves_chinese_characters(self) -> None:
        self.assertEqual(safe_filename("Python 学习笔记！"), "python-学习笔记")
