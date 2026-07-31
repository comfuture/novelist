#!/usr/bin/env python3
"""Export a self-contained Novelist workspace without installing the plugin."""

from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "novelist"
SCAFFOLD_ROOT = PLUGIN_ROOT / "assets" / "scaffold"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
STANDALONE_SKILLS = {
    "analytical-review",
    "create-character",
    "create-material",
    "create-plot",
    "create-setting",
    "create-visual-asset",
    "novel-story-telling",
    "publish-novel",
}
AGENT_CHOICES = ("codex", "claude", "antigravity", "all")


@dataclass(frozen=True)
class CopyItem:
    source: Path
    relative_target: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a standalone Markdown novel workspace with repository-local "
            "Novelist skills."
        )
    )
    parser.add_argument("--destination", required=True, help="Destination workspace")
    parser.add_argument(
        "--agent",
        required=True,
        choices=AGENT_CHOICES,
        help="Agent-local skill layout to export",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace colliding managed files after explicit approval",
    )
    return parser.parse_args()


def source_files(root: Path) -> list[Path]:
    if not root.is_dir() or root.is_symlink():
        raise ValueError(f"source directory is missing or unsafe: {root}")

    resolved_root = root.resolve()
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        relative_path = path.relative_to(root)
        if path.is_symlink():
            raise ValueError(f"source payload contains a symbolic link: {relative_path}")
        if "__pycache__" in relative_path.parts or path.suffix == ".pyc":
            continue
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError(f"source payload contains a non-regular file: {relative_path}")
        if not path.resolve().is_relative_to(resolved_root):
            raise ValueError(f"source payload escapes its root: {relative_path}")
        files.append(path)
    return files


def skill_copy_items(relative_root: Path) -> list[CopyItem]:
    items: list[CopyItem] = []
    for skill_name in sorted(STANDALONE_SKILLS):
        skill_root = SKILLS_ROOT / skill_name
        for source in source_files(skill_root):
            relative_source = source.relative_to(skill_root)
            items.append(
                CopyItem(
                    source=source,
                    relative_target=relative_root / skill_name / relative_source,
                )
            )
    return items


def build_copy_plan(agent: str) -> list[CopyItem]:
    items = [
        CopyItem(source=source, relative_target=source.relative_to(SCAFFOLD_ROOT))
        for source in source_files(SCAFFOLD_ROOT)
    ]

    if agent in {"codex", "antigravity", "all"}:
        items.extend(skill_copy_items(Path(".agents") / "skills"))
    if agent in {"claude", "all"}:
        items.extend(skill_copy_items(Path(".claude") / "skills"))

    plan: dict[Path, Path] = {}
    for item in items:
        previous = plan.get(item.relative_target)
        if previous is not None and previous != item.source:
            raise ValueError(f"conflicting sources for {item.relative_target}")
        plan[item.relative_target] = item.source
    return [
        CopyItem(source=source, relative_target=relative_target)
        for relative_target, source in sorted(plan.items())
    ]


def validate_destination(destination: Path) -> None:
    for candidate in (destination, *destination.parents):
        if candidate.is_symlink():
            raise ValueError(
                f"destination path contains a symbolic-link ancestor: {candidate}"
            )

    resolved_plugin_root = PLUGIN_ROOT.resolve()
    resolved_destination = destination.resolve()
    if resolved_destination == resolved_plugin_root or resolved_destination.is_relative_to(
        resolved_plugin_root
    ):
        raise ValueError("refusing to export inside the Novelist plugin installation")
    if destination.exists() and not destination.is_dir():
        raise ValueError(f"destination root is not a directory: {destination}")


def unsafe_destination_errors(destination: Path, plan: list[CopyItem]) -> list[str]:
    errors: list[str] = []
    resolved_destination = destination.resolve()
    for item in plan:
        target = destination / item.relative_target
        if target.is_symlink():
            errors.append(f"managed target is a symbolic link: {target}")
        elif target.exists() and not target.is_file():
            errors.append(f"managed target is not a regular file: {target}")

        parent = target.parent
        while parent != destination:
            if parent.is_symlink():
                errors.append(f"managed parent is a symbolic link: {parent}")
                break
            if parent.exists() and not parent.is_dir():
                errors.append(f"managed parent is not a directory: {parent}")
                break
            parent = parent.parent

        if not target.parent.resolve().is_relative_to(resolved_destination):
            errors.append(f"managed target escapes the destination: {target}")
    return sorted(set(errors))


def copy_file_atomically(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=target.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "wb") as destination_file:
            with source.open("rb") as source_file:
                shutil.copyfileobj(source_file, destination_file)
        shutil.copystat(source, temporary_path, follow_symlinks=False)
        os.replace(temporary_path, target)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def export(destination: Path, agent: str, *, force: bool) -> list[Path]:
    validate_destination(destination)
    plan = build_copy_plan(agent)
    unsafe_errors = unsafe_destination_errors(destination, plan)
    if unsafe_errors:
        formatted = "\n".join(f"- {error}" for error in unsafe_errors)
        raise ValueError(f"unsafe destination layout; no files were written:\n{formatted}")

    collisions = [
        destination / item.relative_target
        for item in plan
        if (destination / item.relative_target).exists()
    ]
    if collisions and not force:
        formatted = "\n".join(f"- {path}" for path in collisions)
        raise FileExistsError(
            "refusing to overwrite managed files; no files were written:\n"
            f"{formatted}"
        )

    destination.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for item in plan:
        target = destination / item.relative_target
        copy_file_atomically(item.source, target)
        written.append(target)
    return written


def main() -> None:
    args = parse_args()
    destination = Path(args.destination).expanduser().absolute()
    try:
        written = export(destination, args.agent, force=args.force)
    except (FileExistsError, OSError, ValueError) as error:
        print(f"Standalone scaffold export failed: {error}")
        raise SystemExit(1) from error

    top_level_paths = sorted({path.relative_to(destination).parts[0] for path in written})
    print(f"Created standalone Novelist workspace: {destination.resolve()}")
    print(f"Agent mode: {args.agent}")
    print("Created top-level paths:")
    for path in top_level_paths:
        print(f"- {path}")
    print(f"Exported {len(written)} managed files.")


if __name__ == "__main__":
    main()
