#!/usr/bin/env python3
"""Initialize a novel workspace from the scaffold bundled with the plugin."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import date
from pathlib import Path


LANGUAGE_RE = re.compile(r"^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$")
FRONTMATTER_DATE_RE = re.compile(
    r"^(created|updated): \d{4}-\d{2}-\d{2}$",
    flags=re.MULTILINE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Markdown novel project from the Novelist scaffold."
    )
    parser.add_argument("--project-root", required=True, help="Destination project directory")
    parser.add_argument("--title", help="Working title to write to project.md")
    parser.add_argument("--language", help="BCP 47-style language tag for project.md")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace colliding scaffold-managed files after explicit approval",
    )
    return parser.parse_args()


def plugin_root() -> Path:
    return Path(__file__).resolve().parents[3]


def scaffold_files(scaffold_root: Path) -> list[Path]:
    return sorted(path for path in scaffold_root.rglob("*") if path.is_file())


def validate_inputs(args: argparse.Namespace, destination: Path, source_root: Path) -> None:
    if args.title is not None and not args.title.strip():
        raise ValueError("--title must not be empty")
    if args.title is not None and any(character in args.title for character in "\r\n"):
        raise ValueError("--title must fit on one line")
    if args.language is not None and LANGUAGE_RE.fullmatch(args.language) is None:
        raise ValueError("--language must be a BCP 47-style tag such as ko, en, or ko-KR")

    resolved_plugin_root = plugin_root().resolve()
    resolved_destination = destination.resolve()
    if resolved_destination == resolved_plugin_root or resolved_destination.is_relative_to(
        resolved_plugin_root
    ):
        raise ValueError("refusing to initialize inside the Novelist plugin installation")
    if not source_root.is_dir():
        raise ValueError(f"bundled scaffold is missing: {source_root}")


def unsafe_destination_errors(
    destination: Path,
    source_root: Path,
    sources: list[Path],
) -> list[str]:
    errors: list[str] = []
    resolved_destination = destination.resolve()
    if destination.is_symlink():
        errors.append(f"destination root is a symbolic link: {destination}")
    elif destination.exists() and not destination.is_dir():
        errors.append(f"destination root is not a directory: {destination}")

    for source in sources:
        target = destination / source.relative_to(source_root)
        if target.is_symlink():
            errors.append(f"scaffold target is a symbolic link: {target}")
        elif target.exists() and not target.is_file():
            errors.append(f"scaffold target is not a regular file: {target}")

        parent = target.parent
        while parent != destination:
            if parent.is_symlink():
                errors.append(f"scaffold parent is a symbolic link: {parent}")
                break
            if parent.exists() and not parent.is_dir():
                errors.append(f"scaffold parent is not a directory: {parent}")
                break
            parent = parent.parent

        if not target.parent.resolve().is_relative_to(resolved_destination):
            errors.append(f"scaffold target escapes the destination: {target}")

    return sorted(set(errors))


def configure_markdown(path: Path, *, title: str | None, language: str | None) -> None:
    contents = path.read_text(encoding="utf-8")
    today = date.today().isoformat()
    contents = FRONTMATTER_DATE_RE.sub(lambda match: f"{match.group(1)}: {today}", contents)

    if path.name == "project.md":
        if title is not None:
            clean_title = title.strip()
            contents = re.sub(
                r'^title: ".*"$',
                f"title: {json.dumps(clean_title, ensure_ascii=False)}",
                contents,
                count=1,
                flags=re.MULTILINE,
            )
            contents = re.sub(
                r"^# Untitled Novel$",
                f"# {clean_title}",
                contents,
                count=1,
                flags=re.MULTILINE,
            )
        if language is not None:
            contents = re.sub(
                r"^language: .+$",
                f"language: {language}",
                contents,
                count=1,
                flags=re.MULTILINE,
            )

    path.write_text(contents, encoding="utf-8")


def initialize(args: argparse.Namespace) -> list[Path]:
    source_root = plugin_root() / "assets" / "scaffold"
    destination = Path(args.project_root).expanduser().absolute()
    validate_inputs(args, destination, source_root)

    sources = scaffold_files(source_root)
    unsafe_errors = unsafe_destination_errors(destination, source_root, sources)
    if unsafe_errors:
        formatted = "\n".join(f"- {error}" for error in unsafe_errors)
        raise ValueError(f"unsafe destination layout; no files were written:\n{formatted}")

    collisions = [
        destination / source.relative_to(source_root)
        for source in sources
        if (destination / source.relative_to(source_root)).exists()
    ]
    if collisions and not args.force:
        formatted = "\n".join(f"- {path}" for path in collisions)
        raise FileExistsError(
            "refusing to overwrite existing scaffold files; no files were written:\n"
            f"{formatted}"
        )

    destination.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for source in sources:
        relative_path = source.relative_to(source_root)
        target = destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if target.suffix == ".md":
            configure_markdown(target, title=args.title, language=args.language)
        written.append(target)
    return written


def main() -> None:
    args = parse_args()
    try:
        written = initialize(args)
    except (FileExistsError, OSError, ValueError) as error:
        print(f"Novel project initialization failed: {error}")
        raise SystemExit(1) from error

    destination = Path(args.project_root).expanduser().resolve()
    print(f"Initialized novel project: {destination}")
    print(f"Created or replaced {len(written)} scaffold files.")


if __name__ == "__main__":
    main()
