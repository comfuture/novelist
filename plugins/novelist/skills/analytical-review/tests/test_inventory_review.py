"""Regression tests for content-free analytical-review scope inventories."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inventory_review.py"
SPEC = importlib.util.spec_from_file_location("inventory_review_under_test", SCRIPT)
assert SPEC and SPEC.loader
inventory_review = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = inventory_review
SPEC.loader.exec_module(inventory_review)


def write_source(
    path: Path,
    *,
    source_type: str,
    title: str,
    body: str,
    number: int | None = None,
) -> None:
    number_line = f"number: {number}\n" if number is not None else ""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
id: {source_type}-{path.stem}
type: {source_type}
{number_line}title: "{title}"
status: draft
tags: []
created: 2026-01-01
updated: 2026-01-01
---
# {title}

{body}
""",
        encoding="utf-8",
    )


def write_chapter(path: Path, *, number: int, title: str, draft: str) -> None:
    write_source(
        path,
        source_type="chapter",
        title=title,
        number=number,
        body=f"""## Synopsis

Editorial summary.

## Draft

{draft}

## Revision Notes

None.
""",
    )


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ReviewInventoryTests(unittest.TestCase):
    def test_manuscript_inventory_covers_every_numbered_draft_without_copying_prose(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            private_marker = "SENTINEL_PRIVATE_PROSE_MUST_NOT_APPEAR"
            write_chapter(
                root / "chapters" / "001.first-turn.md",
                number=1,
                title="First Turn",
                draft=f"An opening decision. {private_marker}",
            )
            write_chapter(
                root / "chapters" / "002.second-turn.md",
                number=2,
                title="Second Turn",
                draft="A consequence changes the next decision.",
            )
            (root / "chapters" / "_template.md").write_text(
                private_marker,
                encoding="utf-8",
            )

            result = inventory_review.build_inventory(
                root,
                mode="manuscript",
                targets=[],
                chapter_numbers=[],
                max_batch_tokens=20,
            )

            self.assertEqual(result["unit_count"], 2)
            self.assertEqual(result["eligible_unit_count"], 2)
            self.assertTrue(result["coverage_complete"])
            self.assertEqual(
                [unit["path"] for unit in result["units"]],
                ["chapters/001.first-turn.md", "chapters/002.second-turn.md"],
            )
            self.assertTrue(all(unit["review_section"] == "Draft" for unit in result["units"]))
            self.assertTrue(all(unit["line_start"] for unit in result["units"]))
            self.assertGreaterEqual(len(result["batches"]), 2)
            self.assertNotIn(private_marker, str(result))

    def test_outline_mode_inventories_plans_and_never_claims_chapter_draft_scope(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_source(
                root / "plot" / "000.master-plot.md",
                source_type="plot",
                title="Master Plot",
                body="## Promise\n\nA choice changes the relationship.",
            )
            write_source(
                root / "outlines" / "000.master-outline.md",
                source_type="outline",
                title="Master Outline",
                body="## Sequence\n\nA planned consequence follows.",
            )
            write_chapter(
                root / "chapters" / "001.existing-draft.md",
                number=1,
                title="Existing Draft",
                draft="This chapter is outside outline mode.",
            )

            result = inventory_review.build_inventory(
                root,
                mode="outline",
                targets=[],
                chapter_numbers=[],
                max_batch_tokens=12000,
            )

            self.assertEqual(result["unit_count"], 2)
            self.assertTrue(all(unit["review_section"] == "document" for unit in result["units"]))
            self.assertFalse(any(unit["kind"] == "chapter" for unit in result["units"]))

    def test_chapter_mode_requires_and_honors_an_explicit_scope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_chapter(
                root / "chapters" / "001.first.md",
                number=1,
                title="First",
                draft="First draft.",
            )
            write_chapter(
                root / "chapters" / "002.second.md",
                number=2,
                title="Second",
                draft="Second draft.",
            )

            with self.assertRaisesRegex(ValueError, "requires --chapter or --target"):
                inventory_review.build_inventory(
                    root,
                    mode="chapter",
                    targets=[],
                    chapter_numbers=[],
                    max_batch_tokens=12000,
                )

            result = inventory_review.build_inventory(
                root,
                mode="chapter",
                targets=[],
                chapter_numbers=[2],
                max_batch_tokens=12000,
            )
            self.assertEqual([unit["number"] for unit in result["units"]], [2])

    def test_regression_mode_requires_a_bounded_scope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_chapter(
                root / "chapters" / "001.changed.md",
                number=1,
                title="Changed",
                draft="A revised draft.",
            )

            with self.assertRaisesRegex(
                ValueError,
                "regression mode requires --chapter or --target",
            ):
                inventory_review.build_inventory(
                    root,
                    mode="regression",
                    targets=[],
                    chapter_numbers=[],
                    max_batch_tokens=12000,
                )

            result = inventory_review.build_inventory(
                root,
                mode="regression",
                targets=[],
                chapter_numbers=[1],
                max_batch_tokens=12000,
            )
            self.assertEqual([unit["number"] for unit in result["units"]], [1])

    def test_malformed_draft_is_counted_but_not_marked_covered(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_source(
                root / "chapters" / "001.missing-draft.md",
                source_type="chapter",
                title="Missing Draft",
                number=1,
                body="## Synopsis\n\nOnly editorial material.\n\n## Revision Notes\n\nNone.",
            )

            result = inventory_review.build_inventory(
                root,
                mode="manuscript",
                targets=[],
                chapter_numbers=[],
                max_batch_tokens=12000,
            )

            self.assertEqual(result["unit_count"], 1)
            self.assertEqual(result["eligible_unit_count"], 0)
            self.assertFalse(result["coverage_complete"])
            self.assertIn("expected one case-sensitive Draft section", str(result["issues"]))
            self.assertEqual(result["batches"], [])

    def test_numbering_gaps_remain_reviewable_and_oversized_units_are_visible(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_chapter(
                root / "chapters" / "001.first.md",
                number=1,
                title="First",
                draft="Short draft.",
            )
            write_chapter(
                root / "chapters" / "003.third.md",
                number=3,
                title="Third",
                draft="A" * 200,
            )

            result = inventory_review.build_inventory(
                root,
                mode="manuscript",
                targets=[],
                chapter_numbers=[],
                max_batch_tokens=20,
            )

            self.assertTrue(result["coverage_complete"])
            self.assertEqual([unit["number"] for unit in result["units"]], [1, 3])
            self.assertTrue(any(batch["oversized"] for batch in result["batches"]))

    def test_duplicate_chapter_numbers_block_complete_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_chapter(
                root / "chapters" / "001.first.md",
                number=1,
                title="First",
                draft="First version.",
            )
            write_chapter(
                root / "chapters" / "001.alternate.md",
                number=1,
                title="Alternate",
                draft="Alternate version.",
            )

            result = inventory_review.build_inventory(
                root,
                mode="manuscript",
                targets=[],
                chapter_numbers=[],
                max_batch_tokens=12000,
            )

            self.assertFalse(result["coverage_complete"])
            self.assertEqual(result["eligible_unit_count"], 0)
            self.assertIn("duplicate chapter number", str(result["issues"]))

    def test_inventory_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            chapter = root / "chapters" / "001.read-only.md"
            write_chapter(
                chapter,
                number=1,
                title="Read Only",
                draft="The source must remain unchanged.",
            )
            before = file_hash(chapter)

            inventory_review.build_inventory(
                root,
                mode="manuscript",
                targets=[],
                chapter_numbers=[],
                max_batch_tokens=12000,
            )

            self.assertEqual(file_hash(chapter), before)

    def test_target_must_remain_inside_the_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            root.mkdir()
            outside = Path(directory) / "outside.md"
            outside.write_text("# Outside\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "escapes the project root"):
                inventory_review.build_inventory(
                    root,
                    mode="outline",
                    targets=["../outside.md"],
                    chapter_numbers=[],
                    max_batch_tokens=12000,
                )

    def test_target_symbolic_links_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "outlines" / "source.md"
            write_source(
                source,
                source_type="outline",
                title="Source",
                body="## Sequence\n\nA planned change.",
            )
            link = root / "outlines" / "linked.md"
            link.symlink_to(source)

            with self.assertRaisesRegex(ValueError, "must not be a symbolic link"):
                inventory_review.build_inventory(
                    root,
                    mode="outline",
                    targets=["outlines/linked.md"],
                    chapter_numbers=[],
                    max_batch_tokens=12000,
                )

    def test_discovery_does_not_follow_a_symbolic_linked_source_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            outside = Path(directory) / "outside"
            root.mkdir()
            write_chapter(
                outside / "001.external.md",
                number=1,
                title="External",
                draft="This external source must not be inventoried.",
            )
            (root / "chapters").symlink_to(outside)

            with self.assertRaisesRegex(
                ValueError,
                "source directory must not be a symbolic link: chapters",
            ):
                inventory_review.build_inventory(
                    root,
                    mode="manuscript",
                    targets=[],
                    chapter_numbers=[],
                    max_batch_tokens=12000,
                )

    def test_discovery_blocks_a_symbolic_linked_chapter_without_hiding_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            outside = Path(directory) / "outside"
            write_chapter(
                root / "chapters" / "001.local.md",
                number=1,
                title="Local",
                draft="The local source is reviewable.",
            )
            write_chapter(
                outside / "002.external.md",
                number=2,
                title="External",
                draft="This external source must block complete coverage.",
            )
            (root / "chapters" / "002.external.md").symlink_to(
                outside / "002.external.md"
            )

            with self.assertRaisesRegex(
                ValueError,
                "discovered source must not be a symbolic link",
            ):
                inventory_review.build_inventory(
                    root,
                    mode="manuscript",
                    targets=[],
                    chapter_numbers=[],
                    max_batch_tokens=12000,
                )

    def test_cli_refuses_to_persist_inventory_inside_the_reviewed_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_source(
                root / "outlines" / "000.master-outline.md",
                source_type="outline",
                title="Master Outline",
                body="## Sequence\n\nA planned change.",
            )
            with mock.patch.object(
                sys,
                "argv",
                [
                    str(SCRIPT),
                    "--project-root",
                    str(root),
                    "--mode",
                    "outline",
                    "--output",
                    str(root / "review-inventory.json"),
                ],
            ):
                with self.assertRaisesRegex(
                    SystemExit,
                    "--output must remain outside the reviewed project",
                ):
                    inventory_review.main()


if __name__ == "__main__":
    unittest.main()
