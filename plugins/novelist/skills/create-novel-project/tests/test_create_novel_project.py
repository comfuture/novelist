from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "create_novel_project.py"


class CreateNovelProjectTests(unittest.TestCase):
    def run_initializer(self, destination: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--project-root",
                str(destination),
                *arguments,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_initializes_configured_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "book"
            result = self.run_initializer(
                destination,
                "--title",
                "기억의 색인",
                "--language",
                "ko-KR",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            project = (destination / "project.md").read_text(encoding="utf-8")
            self.assertIn('title: "기억의 색인"', project)
            self.assertIn("language: ko-KR", project)
            self.assertIn("# 기억의 색인", project)
            self.assertIn(f"created: {date.today().isoformat()}", project)
            self.assertTrue((destination / "chapters" / "_template.md").is_file())
            self.assertTrue((destination / "published" / ".gitignore").is_file())
            self.assertFalse((destination / ".agents" / "skills").exists())

    def test_collision_preflight_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "book"
            destination.mkdir()
            existing_project = destination / "project.md"
            existing_project.write_text("keep me\n", encoding="utf-8")

            result = self.run_initializer(destination)

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(existing_project.read_text(encoding="utf-8"), "keep me\n")
            self.assertFalse((destination / "chapters").exists())

    def test_force_rejects_symlink_escape_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            destination = temporary_root / "book"
            outside = temporary_root / "outside"
            destination.mkdir()
            outside.mkdir()
            (destination / "assets").symlink_to(outside, target_is_directory=True)

            result = self.run_initializer(destination, "--force")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symbolic link", result.stdout)
            self.assertFalse((destination / "project.md").exists())
            self.assertEqual(list(outside.iterdir()), [])

    def test_rejects_multiline_title_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "book"

            result = self.run_initializer(destination, "--title", "Line one\nLine two")

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
