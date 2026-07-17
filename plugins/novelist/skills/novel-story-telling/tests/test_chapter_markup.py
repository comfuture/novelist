"""Regression tests for chapter prose Markdown guardrails."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "check_continuity_under_test",
    SCRIPTS / "check_continuity.py",
)
assert SPEC and SPEC.loader
check_continuity = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = check_continuity
SPEC.loader.exec_module(check_continuity)


class DraftMarkupTests(unittest.TestCase):
    def test_canonical_prose_markup_is_accepted(self) -> None:
        draft = """Narration.

*“Spoken dialogue.”*

*“승인해.”* 레아가 말했다.

레아가 물었다. *“정말?”*

*An interior thought.*

**Semantic emphasis** and `machine.literal`.

---

A new scene.
"""
        self.assertEqual(check_continuity.draft_markup_issues(draft), [])

    def test_dialogue_requires_an_italic_curly_quote_span(self) -> None:
        invalid = (
            "“Plain dialogue.”",
            "Narration. “Inline dialogue.”",
            '*"Straight dialogue."*',
            "*“”*",
            "**“Bold dialogue.”**",
        )
        for draft in invalid:
            with self.subTest(draft=draft):
                codes = {
                    code
                    for code, _line, _message in check_continuity.draft_markup_issues(draft)
                }
                self.assertTrue(
                    {"chapter-dialogue-format", "chapter-dialogue-quotes"} & codes
                )

    def test_dialogue_follows_normal_markdown_paragraph_boundaries(self) -> None:
        draft = "Narration.\n*“The same paragraph after a soft break.”*"
        self.assertEqual(check_continuity.draft_markup_issues(draft), [])

    def test_dialogue_allows_nested_single_quotes_and_ignores_code_quotes(self) -> None:
        draft = """*“그는 ‘가지 마’라고 말했다.”*

The log emitted `“READY”`.
"""
        self.assertEqual(check_continuity.draft_markup_issues(draft), [])

    def test_five_dialogue_only_paragraphs_require_a_readability_break(self) -> None:
        draft = "\n\n".join(f"*“Line {index}.”*" for index in range(1, 6))
        findings = check_continuity.draft_markup_issues(draft)
        self.assertIn(
            "chapter-dialogue-attribution",
            {code for code, _line, _message in findings},
        )

    def test_attribution_breaks_a_dialogue_only_run(self) -> None:
        draft = """*“One.”*

*“Two.”*

*“Three.”*

*“Four.”*

*“Five.”* Rhea crossed her arms.
"""
        self.assertEqual(check_continuity.draft_markup_issues(draft), [])

    def test_legacy_scene_break_is_rejected(self) -> None:
        findings = check_continuity.draft_markup_issues("Before.\n\n* * *\n\nAfter.")
        self.assertIn("chapter-scene-break", {code for code, _line, _message in findings})

    def test_prose_list_blockquote_fence_and_unbalanced_markers_are_rejected(self) -> None:
        draft = """- dialogue disguised as a list

> dialogue disguised as a quote

```
log
```

*unfinished thought

`unfinished literal
"""
        codes = {code for code, _line, _message in check_continuity.draft_markup_issues(draft)}
        self.assertTrue(
            {
                "chapter-prose-list",
                "chapter-prose-blockquote",
                "chapter-prose-code-block",
                "chapter-italics",
                "chapter-inline-code",
            }.issubset(codes)
        )

    def test_scene_break_requires_blank_lines(self) -> None:
        findings = check_continuity.draft_markup_issues("Before.\n---\nAfter.")
        self.assertIn(
            "chapter-scene-break-spacing",
            {code for code, _line, _message in findings},
        )

    def test_additional_h2_section_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            chapters = root / "chapters"
            chapters.mkdir()
            (chapters / "001.test.md").write_text(
                '''---
id: chapter-001
type: chapter
number: 1
title: "Test"
slug: test
status: draft
pov: ""
timeline: ""
setting: ""
word_target: 100
characters: []
materials: []
macguffins: []
plot_threads: []
outline: ""
published: false
created: 2026-07-15
updated: 2026-07-15
tags: []
---
# Test

## Synopsis

Synopsis.

## Draft

This text would be published.

## Interlude

This text must not be silently omitted.

## Revision Notes

None.
''',
                encoding="utf-8",
            )

            report = check_continuity.audit(root)
            codes = {finding["code"] for finding in report["issues"]}
            self.assertIn("chapter-section-layout", codes)


if __name__ == "__main__":
    unittest.main()
