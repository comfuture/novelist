#!/usr/bin/env python3
"""Synchronize canonical novel skills and scaffold files into the plugin."""

from __future__ import annotations

import argparse
import filecmp
import shutil
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILLS_ROOT = REPOSITORY_ROOT / ".agents" / "skills"
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "novelist"
PLUGIN_SKILLS_ROOT = PLUGIN_ROOT / "skills"
SCAFFOLD_ROOT = PLUGIN_ROOT / "assets" / "scaffold"

PLUGIN_ONLY_SKILLS = {"create-novel-project"}
MANUAL_SCAFFOLD_FILES = {
    Path("AGENTS.md"),
    Path("README.md"),
}
SCAFFOLD_FILES = {
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
        description="Synchronize or verify the checked-in Novelist plugin payload."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report drift without changing files.",
    )
    return parser.parse_args()


def canonical_skill_names() -> set[str]:
    return {
        path.name
        for path in SOURCE_SKILLS_ROOT.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }


def compare_directories(source: Path, target: Path) -> list[str]:
    if not target.is_dir():
        return [f"missing directory: {target.relative_to(REPOSITORY_ROOT)}"]

    errors: list[str] = []
    source_entries = {path.name: path for path in source.iterdir()}
    target_entries = {path.name: path for path in target.iterdir()}

    for name in sorted(source_entries.keys() - target_entries.keys()):
        errors.append(f"missing from plugin: {(target / name).relative_to(REPOSITORY_ROOT)}")
    for name in sorted(target_entries.keys() - source_entries.keys()):
        errors.append(f"unexpected in plugin: {(target / name).relative_to(REPOSITORY_ROOT)}")

    for name in sorted(source_entries.keys() & target_entries.keys()):
        source_path = source_entries[name]
        target_path = target_entries[name]
        if source_path.is_dir() and target_path.is_dir():
            errors.extend(compare_directories(source_path, target_path))
        elif source_path.is_file() and target_path.is_file():
            if not filecmp.cmp(source_path, target_path, shallow=False):
                errors.append(
                    f"content drift: {target_path.relative_to(REPOSITORY_ROOT)}"
                )
        else:
            errors.append(f"type drift: {target_path.relative_to(REPOSITORY_ROOT)}")
    return errors


def check() -> list[str]:
    errors: list[str] = []
    skill_names = canonical_skill_names()

    for name in sorted(skill_names):
        errors.extend(
            compare_directories(SOURCE_SKILLS_ROOT / name, PLUGIN_SKILLS_ROOT / name)
        )

    if PLUGIN_SKILLS_ROOT.is_dir():
        actual_skill_names = {
            path.name
            for path in PLUGIN_SKILLS_ROOT.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        }
        for name in sorted(actual_skill_names - skill_names - PLUGIN_ONLY_SKILLS):
            errors.append(f"unexpected plugin skill: plugins/novelist/skills/{name}")

    for relative_path in sorted(SCAFFOLD_FILES):
        source = REPOSITORY_ROOT / relative_path
        target = SCAFFOLD_ROOT / relative_path
        if not target.is_file():
            errors.append(f"missing scaffold file: {target.relative_to(REPOSITORY_ROOT)}")
        elif not filecmp.cmp(source, target, shallow=False):
            errors.append(f"scaffold drift: {target.relative_to(REPOSITORY_ROOT)}")

    for relative_path in sorted(MANUAL_SCAFFOLD_FILES):
        target = SCAFFOLD_ROOT / relative_path
        if not target.is_file():
            errors.append(f"missing plugin-aware scaffold file: {target.relative_to(REPOSITORY_ROOT)}")

    allowed_scaffold_files = SCAFFOLD_FILES | MANUAL_SCAFFOLD_FILES
    if SCAFFOLD_ROOT.is_dir():
        actual_scaffold_files = {
            path.relative_to(SCAFFOLD_ROOT)
            for path in SCAFFOLD_ROOT.rglob("*")
            if path.is_file()
        }
        for relative_path in sorted(actual_scaffold_files - allowed_scaffold_files):
            errors.append(
                f"unexpected scaffold file: "
                f"{(SCAFFOLD_ROOT / relative_path).relative_to(REPOSITORY_ROOT)}"
            )

    return errors


def sync() -> None:
    skill_names = canonical_skill_names()
    PLUGIN_SKILLS_ROOT.mkdir(parents=True, exist_ok=True)

    for path in PLUGIN_SKILLS_ROOT.iterdir():
        if path.is_dir() and path.name not in skill_names | PLUGIN_ONLY_SKILLS:
            shutil.rmtree(path)

    for name in sorted(skill_names):
        source = SOURCE_SKILLS_ROOT / name
        target = PLUGIN_SKILLS_ROOT / name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)

    SCAFFOLD_ROOT.mkdir(parents=True, exist_ok=True)
    for relative_path in sorted(SCAFFOLD_FILES):
        source = REPOSITORY_ROOT / relative_path
        target = SCAFFOLD_ROOT / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    allowed_scaffold_files = SCAFFOLD_FILES | MANUAL_SCAFFOLD_FILES
    for path in sorted(SCAFFOLD_ROOT.rglob("*"), reverse=True):
        if path.is_file() and path.relative_to(SCAFFOLD_ROOT) not in allowed_scaffold_files:
            path.unlink()
        elif path.is_dir() and not any(path.iterdir()):
            path.rmdir()


def main() -> None:
    args = parse_args()
    if not args.check:
        sync()

    errors = check()
    if errors:
        print("Novelist plugin synchronization check failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    if args.check:
        print("Novelist plugin is synchronized.")
    else:
        print("Synchronized Novelist plugin skills and scaffold files.")


if __name__ == "__main__":
    main()
