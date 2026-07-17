"""Regression tests for editorial reader-model state in the story ledger."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "update_story_ledger_under_test",
    SCRIPTS / "update_story_ledger.py",
)
assert SPEC and SPEC.loader
update_story_ledger = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = update_story_ledger
SPEC.loader.exec_module(update_story_ledger)


class ReaderModelLedgerTests(unittest.TestCase):
    def test_reader_model_state_is_rendered_as_editorial(self) -> None:
        section = update_story_ledger.render_section(
            {
                "chapter": 3,
                "title": "A Changed Picture",
                "summary": "The witness contradicts the official account.",
                "reader_model_changes": [
                    {
                        "id": "reader-witness-doubt",
                        "status": "expected",
                        "evidence": "The witness repeats two phrases from the official statement.",
                        "expected_inference": "The reader can suspect the witness was coached.",
                        "uncertainty": "The repetition could still be coincidental.",
                    }
                ],
                "open_reader_questions": ["Who supplied the repeated phrases?"],
            }
        )

        self.assertIn(
            "### Reader Evidence And Expected Inference (Editorial)", section
        )
        self.assertIn("reader-witness-doubt [expected]", section)
        self.assertIn("Evidence: The witness repeats two phrases", section)
        self.assertIn("Expected inference: The reader can suspect", section)
        self.assertIn("Uncertainty: The repetition could still be coincidental", section)
        self.assertIn("### Open Reader Questions (Editorial)", section)
        self.assertIn("Who supplied the repeated phrases?", section)

    def test_initial_ledger_does_not_treat_reader_inference_as_canon(self) -> None:
        document = update_story_ledger.initial_document("2026-07-15")

        self.assertIn("Reader-model entries are editorial hypotheses, not canon facts", document)
        self.assertIn("reader-visible Draft evidence", document)


if __name__ == "__main__":
    unittest.main()
