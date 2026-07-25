from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY_ROOT / "scripts" / "create_scaffold.py"
SHELL_WRAPPER = REPOSITORY_ROOT / "scripts" / "create-scaffold.sh"
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "novelist"
SCAFFOLD_ROOT = PLUGIN_ROOT / "assets" / "scaffold"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
STANDALONE_SKILLS = {
    "create-character",
    "create-material",
    "create-plot",
    "create-setting",
    "create-visual-asset",
    "novel-story-telling",
    "publish-novel",
}


def regular_relative_files(root: Path) -> set[Path]:
    return {
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink() and "__pycache__" not in path.parts
    }


class CreateScaffoldTests(unittest.TestCase):
    def run_exporter(
        self,
        destination: Path,
        agent: str,
        *arguments: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--destination",
                str(destination),
                "--agent",
                agent,
                *arguments,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def expected_files(self, agent: str) -> set[Path]:
        expected = regular_relative_files(SCAFFOLD_ROOT)
        for skill_name in STANDALONE_SKILLS:
            skill_files = regular_relative_files(SKILLS_ROOT / skill_name)
            if agent in {"codex", "antigravity", "all"}:
                expected.update(
                    Path(".agents") / "skills" / skill_name / path for path in skill_files
                )
            if agent in {"claude", "all"}:
                expected.update(
                    Path(".claude") / "skills" / skill_name / path for path in skill_files
                )
        return expected

    def test_each_agent_mode_exports_the_exact_file_set(self) -> None:
        for agent in ("codex", "claude", "antigravity", "all"):
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as temporary_directory:
                destination = Path(temporary_directory) / "book"
                result = self.run_exporter(destination, agent)

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(f"Agent mode: {agent}", result.stdout)
                self.assertEqual(regular_relative_files(destination), self.expected_files(agent))
                self.assertFalse(
                    (destination / ".agents" / "skills" / "create-novel-project").exists()
                )
                self.assertFalse(
                    (destination / ".claude" / "skills" / "create-novel-project").exists()
                )
                self.assertFalse((destination / ".codex-plugin").exists())
                self.assertFalse((destination / ".claude-plugin").exists())
                self.assertFalse((destination / "submission").exists())
                self.assertFalse((destination / ".git").exists())

    def test_exported_files_match_the_canonical_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "book"
            result = self.run_exporter(destination, "all")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            for relative_path in regular_relative_files(SCAFFOLD_ROOT):
                self.assertEqual(
                    (destination / relative_path).read_bytes(),
                    (SCAFFOLD_ROOT / relative_path).read_bytes(),
                )
            for skill_name in STANDALONE_SKILLS:
                for relative_path in regular_relative_files(SKILLS_ROOT / skill_name):
                    source = SKILLS_ROOT / skill_name / relative_path
                    self.assertEqual(
                        (
                            destination
                            / ".agents"
                            / "skills"
                            / skill_name
                            / relative_path
                        ).read_bytes(),
                        source.read_bytes(),
                    )
                    self.assertEqual(
                        (
                            destination
                            / ".claude"
                            / "skills"
                            / skill_name
                            / relative_path
                        ).read_bytes(),
                        source.read_bytes(),
                    )

    def test_collision_in_one_layout_writes_nothing_else(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "book"
            collision = destination / ".claude" / "skills" / "create-character" / "SKILL.md"
            collision.parent.mkdir(parents=True)
            collision.write_text("keep me\n", encoding="utf-8")

            result = self.run_exporter(destination, "all")

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(collision.read_text(encoding="utf-8"), "keep me\n")
            self.assertFalse((destination / "project.md").exists())
            self.assertFalse((destination / ".agents").exists())

    def test_force_replaces_managed_file_without_mutating_hardlink_peer(self) -> None:
        if not hasattr(os, "link"):
            self.skipTest("hard links are not available")
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            destination = temporary_root / "book"
            destination.mkdir()
            outside = temporary_root / "outside-project.md"
            outside.write_text("keep peer\n", encoding="utf-8")
            os.link(outside, destination / "project.md")
            unrelated = destination / "notes.txt"
            unrelated.write_text("keep unrelated\n", encoding="utf-8")

            result = self.run_exporter(destination, "codex", "--force")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(outside.read_text(encoding="utf-8"), "keep peer\n")
            self.assertEqual(unrelated.read_text(encoding="utf-8"), "keep unrelated\n")
            self.assertEqual(
                (destination / "project.md").read_bytes(),
                (SCAFFOLD_ROOT / "project.md").read_bytes(),
            )

    @unittest.skipIf(os.name == "nt", "symlink creation is not reliably available")
    def test_symlinked_target_is_rejected_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            destination = temporary_root / "book"
            outside = temporary_root / "outside"
            destination.mkdir()
            outside.mkdir()
            (destination / "assets").symlink_to(outside, target_is_directory=True)

            result = self.run_exporter(destination, "codex", "--force")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symbolic link", result.stdout)
            self.assertFalse((destination / "project.md").exists())
            self.assertEqual(list(outside.iterdir()), [])

    def test_destination_inside_plugin_is_rejected(self) -> None:
        destination = PLUGIN_ROOT / "temporary-export-test"
        result = self.run_exporter(destination, "codex")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("plugin installation", result.stdout)
        self.assertFalse(destination.exists())

    def test_export_is_self_contained_after_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "book"
            result = self.run_exporter(destination, "codex")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            writer = (
                destination
                / ".agents"
                / "skills"
                / "create-character"
                / "scripts"
                / "write_character.py"
            )
            writer_result = subprocess.run(
                [sys.executable, str(writer), "--help"],
                cwd=destination,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                writer_result.returncode,
                0,
                writer_result.stdout + writer_result.stderr,
            )

    @unittest.skipIf(os.name == "nt", "POSIX wrapper test")
    def test_posix_wrapper_passes_arguments_and_exit_status(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "book"
            result = subprocess.run(
                [
                    "sh",
                    str(SHELL_WRAPPER),
                    "--destination",
                    str(destination),
                    "--agent",
                    "antigravity",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Agent mode: antigravity", result.stdout)
            self.assertTrue((destination / ".agents" / "skills").is_dir())


if __name__ == "__main__":
    unittest.main()
