from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPOSITORY_ROOT / "scripts" / "sync_novelist_plugin.py"
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "novelist"


class PluginPackageTests(unittest.TestCase):
    def test_canonical_plugin_payload_passes_exact_validation(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--check"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("canonical, complete, and self-contained", result.stdout)

    def test_host_manifests_share_version_but_not_schema(self) -> None:
        codex = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        claude = json.loads(
            (PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        claude_marketplace = json.loads(
            (REPOSITORY_ROOT / ".claude-plugin" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        antigravity = json.loads(
            (PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8")
        )

        self.assertEqual(codex["version"], "0.2.0")
        self.assertEqual(claude["version"], "0.2.0")
        self.assertEqual(claude_marketplace["version"], "0.2.0")
        self.assertEqual(claude_marketplace["plugins"][0]["version"], "0.2.0")
        self.assertEqual(
            set(antigravity),
            {"$schema", "name", "description"},
        )
        self.assertNotIn("interface", claude)
        self.assertNotIn("version", antigravity)

    def test_root_is_not_a_duplicate_novel_workspace(self) -> None:
        for relative_path in (
            ".agents/skills",
            "assets",
            "chapters",
            "characters",
            "macguffins",
            "materials",
            "outlines",
            "plot",
            "project.md",
            "published",
            "style",
            "world",
        ):
            path = REPOSITORY_ROOT / relative_path
            if path.is_dir():
                self.assertFalse(
                    any(
                        candidate.is_file() or candidate.is_symlink()
                        for candidate in path.rglob("*")
                    ),
                    relative_path,
                )
            else:
                self.assertFalse(path.exists(), relative_path)

    def test_readmes_do_not_use_source_frontmatter(self) -> None:
        for path in (
            REPOSITORY_ROOT / "README.md",
            PLUGIN_ROOT / "README.md",
            PLUGIN_ROOT / "assets" / "scaffold" / "README.md",
            PLUGIN_ROOT / "assets" / "scaffold" / "published" / "README.md",
        ):
            self.assertFalse(path.read_text(encoding="utf-8").startswith("---\n"), path)

    def test_visual_workflow_is_provider_neutral(self) -> None:
        skill = (
            PLUGIN_ROOT / "skills" / "create-visual-asset" / "SKILL.md"
        ).read_text(encoding="utf-8")
        external_guide = (
            PLUGIN_ROOT
            / "skills"
            / "create-visual-asset"
            / "references"
            / "external-image-provider.md"
        ).read_text(encoding="utf-8")

        self.assertIn("<PROVIDER>_API_KEY", external_guide)
        self.assertIn("no image was generated", skill)
        for provider_name in ("OpenAI", "Gemini", "Stability", "Midjourney"):
            self.assertNotIn(provider_name, external_guide)


if __name__ == "__main__":
    unittest.main()
