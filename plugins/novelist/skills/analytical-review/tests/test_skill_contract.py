"""Static contract tests for analytical-review routing and report semantics."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SKILLS_ROOT = SKILL_ROOT.parent


class AnalyticalReviewSkillContractTests(unittest.TestCase):
    def test_skill_has_complete_trigger_and_language_contracts(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertNotIn("TODO", skill)
        self.assertIn("explicitly requests critique", skill)
        self.assertIn("fully autonomous workflow", skill)
        self.assertIn("Do not invoke this skill automatically", skill)
        self.assertIn("the language explicitly requested by the author", skill)
        self.assertIn("the dominant language of the reviewed source", skill)

    def test_report_contract_preserves_localized_three_section_order(self) -> None:
        report = (SKILL_ROOT / "references" / "report-contract.md").read_text(
            encoding="utf-8"
        )

        positions = [
            report.index("`overall_assessment`"),
            report.index("`work_examination`"),
            report.index("`line_editing`"),
        ]
        self.assertEqual(positions, sorted(positions))
        self.assertRegex(report, r"Localize headings\s+naturally")
        self.assertIn("confidence: confirmed | likely | unresolved", report)
        korean_positions = [
            report.index("`작품 총평`"),
            report.index("`작품 검토`"),
            report.index("`문면 교열`"),
        ]
        self.assertEqual(korean_positions, sorted(korean_positions))

    def test_outline_mode_defers_unwritten_prose_judgments(self) -> None:
        modes = (SKILL_ROOT / "references" / "review-modes.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Explicitly defer prose", modes)
        self.assertIn("dialogue quality", modes)
        self.assertIn("diction", modes)
        self.assertIn("scene-level sentence judgment", modes)

    def test_routing_keeps_ordinary_publication_outside_review(self) -> None:
        modes = (SKILL_ROOT / "references" / "review-modes.md").read_text(
            encoding="utf-8"
        )

        self.assertRegex(
            modes,
            re.compile(
                r"Ordinary publish, export, build, regenerate, package, or validate "
                r"request \| No"
            ),
        )
        self.assertIn("Do not infer the fully", modes)
        self.assertIn("complete novel lifecycle", modes)

    def test_openai_prompt_uses_the_real_skill_name(self) -> None:
        metadata = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("$analytical-review", metadata)
        self.assertNotIn("Use -review", metadata)

    def test_storytelling_and_publication_preserve_the_routing_boundary(self) -> None:
        storytelling = (
            PLUGIN_SKILLS_ROOT / "novel-story-telling" / "SKILL.md"
        ).read_text(encoding="utf-8")
        publication = (PLUGIN_SKILLS_ROOT / "publish-novel" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("fully autonomous start-to-publication request only", storytelling)
        self.assertIn("does not by itself authorize this loop", storytelling)
        self.assertIn("Do not invoke `analytical-review` merely because", publication)
        self.assertIn("Keep literary judgment out of `build_epub.py`", publication)

    def test_review_and_publish_hands_off_without_implied_revision(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        modes = (SKILL_ROOT / "references" / "review-modes.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("explicit review-and-publish request", skill)
        self.assertIn("leave all literary findings unapplied", skill)
        self.assertIn("then pass the unchanged manuscript", modes)
        self.assertIn("ordinary `publish-novel` preflight", modes)

    def test_skill_payload_contains_no_user_specific_absolute_paths(self) -> None:
        forbidden = (
            "/" + "Users" + "/",
            "/" + "home" + "/",
            "Desktop" + "/",
        )
        for path in SKILL_ROOT.rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".py", ".yaml"}:
                continue
            text = path.read_text(encoding="utf-8")
            for value in forbidden:
                with self.subTest(path=path, value=value):
                    self.assertNotIn(value, text)


if __name__ == "__main__":
    unittest.main()
