#!/usr/bin/env python3
"""Validate the canonical, self-contained Novelist plugin payload."""

from __future__ import annotations

import argparse
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "novelist"
PLUGIN_SKILLS_ROOT = PLUGIN_ROOT / "skills"
SCAFFOLD_ROOT = PLUGIN_ROOT / "assets" / "scaffold"

EXPECTED_SKILLS = {
    "create-character",
    "create-material",
    "create-novel-project",
    "create-plot",
    "create-setting",
    "create-visual-asset",
    "novel-story-telling",
    "publish-novel",
}

SCAFFOLD_FILES = {
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path("README.md"),
    Path("project.md"),
    Path("assets/cover/.gitkeep"),
    Path("assets/illustrations/.gitkeep"),
    Path("chapters/_template.md"),
    Path("characters/_template.md"),
    Path("macguffins/_template.md"),
    Path("materials/_template.md"),
    Path("outlines/000.master-outline.md"),
    Path("outlines/_chapter-outline-template.md"),
    Path("plot/000.master-plot.md"),
    Path("plot/_template.md"),
    Path("published/.gitignore"),
    Path("published/README.md"),
    Path("style/000.style-guide.md"),
    Path("style/visual-style-guide.md"),
    Path("world/_template.md"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the canonical Novelist plugin payload."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compatibility flag; validation is always read-only.",
    )
    return parser.parse_args()


def regular_files(root: Path) -> set[Path]:
    if not root.is_dir():
        return set()
    return {
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink()
    }


def symlinks(root: Path) -> set[Path]:
    if not root.is_dir():
        return set()
    return {path.relative_to(root) for path in root.rglob("*") if path.is_symlink()}


def check() -> list[str]:
    errors: list[str] = []

    actual_skill_names = (
        {
            path.name
            for path in PLUGIN_SKILLS_ROOT.iterdir()
            if path.is_dir() and not path.is_symlink() and not path.name.startswith(".")
        }
        if PLUGIN_SKILLS_ROOT.is_dir()
        else set()
    )
    for name in sorted(EXPECTED_SKILLS - actual_skill_names):
        errors.append(f"missing plugin skill: plugins/novelist/skills/{name}")
    for name in sorted(actual_skill_names - EXPECTED_SKILLS):
        errors.append(f"unexpected plugin skill: plugins/novelist/skills/{name}")

    for name in sorted(EXPECTED_SKILLS & actual_skill_names):
        skill_root = PLUGIN_SKILLS_ROOT / name
        skill_file = skill_root / "SKILL.md"
        if not skill_file.is_file() or skill_file.is_symlink():
            errors.append(f"missing regular skill file: {skill_file.relative_to(REPOSITORY_ROOT)}")
        for relative_path in sorted(symlinks(skill_root)):
            errors.append(
                "plugin skills must not contain symbolic links: "
                f"{(skill_root / relative_path).relative_to(REPOSITORY_ROOT)}"
            )
    actual_scaffold_files = regular_files(SCAFFOLD_ROOT)
    for relative_path in sorted(SCAFFOLD_FILES - actual_scaffold_files):
        errors.append(f"missing scaffold file: plugins/novelist/assets/scaffold/{relative_path}")
    for relative_path in sorted(actual_scaffold_files - SCAFFOLD_FILES):
        errors.append(
            f"unexpected scaffold file: plugins/novelist/assets/scaffold/{relative_path}"
        )
    for relative_path in sorted(symlinks(SCAFFOLD_ROOT)):
        errors.append(
            "canonical scaffold must not contain symbolic links: "
            f"plugins/novelist/assets/scaffold/{relative_path}"
        )

    return errors


def main() -> None:
    parse_args()
    errors = check()
    if errors:
        print("Novelist plugin validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Novelist plugin payload is canonical, complete, and self-contained.")


if __name__ == "__main__":
    main()
