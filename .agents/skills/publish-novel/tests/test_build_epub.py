"""Regression tests for Draft-only EPUB packaging and Markdown rendering."""

from __future__ import annotations

import argparse
import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_epub.py"
SPEC = importlib.util.spec_from_file_location("build_epub_under_test", SCRIPT)
assert SPEC and SPEC.loader
build_epub = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = build_epub
SPEC.loader.exec_module(build_epub)


class DraftExtractionTests(unittest.TestCase):
    def test_extracts_only_draft_and_preserves_nested_heading(self) -> None:
        body = """# Test

## Synopsis

SYNOPSIS-SENTINEL

## Draft

DRAFT-SENTINEL

### Nested scene

Nested prose.

## Revision Notes

REVISION-SENTINEL
"""
        draft = build_epub.extract_draft_section(body, Path("001.test.md"))
        self.assertIn("DRAFT-SENTINEL", draft)
        self.assertIn("### Nested scene", draft)
        self.assertNotIn("SYNOPSIS-SENTINEL", draft)
        self.assertNotIn("REVISION-SENTINEL", draft)

    def test_ignores_draft_heading_inside_fenced_code(self) -> None:
        body = """# Test

## Synopsis

```text
## Draft
not a section
```

## Draft

Publish me.

## Revision Notes

None.
"""
        self.assertEqual(
            build_epub.extract_draft_section(body, Path("001.test.md")),
            "Publish me.",
        )

    def test_missing_duplicate_case_mismatch_and_empty_draft_fail(self) -> None:
        invalid_bodies = (
            "# Test\n\n## Synopsis\n\nNo draft.\n",
            "# Test\n\n## Draft\n\nOne\n\n## Draft\n\nTwo\n",
            "# Test\n\n## draft\n\nWrong case.\n",
            "# Test\n\n## Draft\n\n   \n\n## Revision Notes\n\nNone.\n",
            (
                "# Test\n\n## Synopsis\n\nSummary.\n\n## Draft\n\nKeep.\n\n"
                "## Interlude\n\nDo not drop this.\n\n## Revision Notes\n\nNone.\n"
            ),
        )
        for body in invalid_bodies:
            with self.subTest(body=body), self.assertRaises(SystemExit):
                build_epub.extract_draft_section(body, Path("001.test.md"))


class MarkdownRenderingTests(unittest.TestCase):
    def render(self, body: str) -> str:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            return build_epub.render_markdown(
                body,
                root / "chapters" / "001.test.md",
                root,
                {},
                set(),
            )

    def test_thematic_break_precedes_list_parsing(self) -> None:
        rendered = self.render("Before.\n\n* * *\n\nAfter.")
        self.assertEqual(rendered.count('<hr class="scene-break" />'), 1)
        self.assertNotIn("<ul>", rendered)
        self.assertNotIn("<li>", rendered)
        self.assertNotIn("<em>", rendered)

    def test_canonical_scene_break_and_real_list_remain_distinct(self) -> None:
        rendered = self.render("---")
        self.assertIn('<hr class="scene-break" />', rendered)
        self.assertIn(
            '<span class="scene-ornament" aria-hidden="true">* * *</span>',
            rendered,
        )
        self.assertIn("<li>item</li>", self.render("* item"))

    def test_inline_code_is_not_reparsed_as_emphasis(self) -> None:
        rendered = self.render("`*literal*` and *thought*")
        self.assertIn("<code>*literal*</code>", rendered)
        self.assertIn("<em>thought</em>", rendered)
        self.assertNotIn("<code><em>", rendered)

    def test_dialogue_span_and_inner_thought_use_distinct_inline_markup(self) -> None:
        rendered = self.render(
            "Narration.\n\n*“Spoken dialogue.”* The speaker said.\n\n"
            "*Interior thought.*"
        )
        self.assertIn('<p class="prose">Narration.</p>', rendered)
        self.assertIn(
            '<p class="prose"><i class="dialog">“Spoken dialogue.”</i> '
            "The speaker said.</p>",
            rendered,
        )
        self.assertIn(
            '<p class="prose"><em>Interior thought.</em></p>', rendered
        )

    def test_stylesheet_distinguishes_narration_dialogue_and_scene_ornament(self) -> None:
        css = build_epub.stylesheet()
        self.assertIn(".chapter-title", css)
        self.assertIn(".chapter-body i.dialog", css)
        self.assertIn(".scene-ornament", css)
        self.assertIn('"Noto Sans CJK KR"', css)
        self.assertIn('"Noto Serif CJK KR"', css)
        self.assertNotIn("@import", css)
        self.assertNotIn("url(", css)


class EpubIntegrationTests(unittest.TestCase):
    def test_epub_contains_draft_only_and_skips_editorial_images(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            chapters = root / "chapters"
            chapters.mkdir()
            (chapters / "001.test.md").write_text(
                """---
number: 1
title: "Test Chapter"
---
# Test Chapter

## Synopsis

SYNOPSIS-SENTINEL

![missing editorial image](missing-synopsis.png)

## Draft

DRAFT-SENTINEL

---

The published paragraph.

*“The spoken range.”* The speaker said.

*The inward thought.*

## Revision Notes

REVISION-SENTINEL

![another missing image](missing-notes.png)
""",
                encoding="utf-8",
            )
            args = argparse.Namespace(
                project_root=root,
                chapters_dir="chapters",
                staging_dir="published/epub",
                output="published/test.epub",
                cover=None,
                title="Test Book",
                author="Test Author",
                language="en",
            )

            output = build_epub.build(args)
            report = build_epub.validate_epub(output)
            self.assertEqual(report["chapters"], 1)
            self.assertEqual(report["dialogue"], 1)
            self.assertEqual(report["images"], 0)
            self.assertEqual(report["scene_breaks"], 1)

            with zipfile.ZipFile(output) as archive:
                chapter = archive.read("OEBPS/chapters/chapter-001.xhtml").decode("utf-8")
            self.assertIn('<p class="chapter-number">Chapter 1</p>', chapter)
            self.assertIn('<h1 class="chapter-title">Test Chapter</h1>', chapter)
            self.assertIn("DRAFT-SENTINEL", chapter)
            self.assertIn(
                '<p class="prose"><i class="dialog">“The spoken range.”</i> '
                "The speaker said.</p>",
                chapter,
            )
            self.assertIn(
                '<p class="prose"><em>The inward thought.</em></p>', chapter
            )
            self.assertIn('<hr class="scene-break" />', chapter)
            self.assertIn(
                '<span class="scene-ornament" aria-hidden="true">* * *</span>',
                chapter,
            )
            self.assertNotIn("SYNOPSIS-SENTINEL", chapter)
            self.assertNotIn("REVISION-SENTINEL", chapter)
            self.assertNotIn("## Draft", chapter)


if __name__ == "__main__":
    unittest.main()
