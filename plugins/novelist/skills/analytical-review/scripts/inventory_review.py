#!/usr/bin/env python3
"""Build a content-free, bounded inventory for analytical novel review."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


CHAPTER_RE = re.compile(r"^(\d{3})\.([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
MODES = ("outline", "chapter", "manuscript", "regression")


@dataclass(frozen=True)
class Section:
    title: str
    content: str
    start_line: int
    end_line: int


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "none", "~"}:
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            inner = value[1:-1].strip()
            return [] if not inner else [parse_scalar(item) for item in inner.split(",")]
        return parsed if isinstance(parsed, list) else value
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str, int]:
    """Return metadata, body, and the one-based line where the body starts."""
    if not text.startswith("---\n"):
        return {}, text, 1
    lines = text.splitlines(keepends=True)
    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.rstrip() == "---"),
        None,
    )
    if closing_index is None:
        return {}, text, 1

    metadata: dict[str, Any] = {}
    active_list: str | None = None
    for raw_line in lines[1:closing_index]:
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        list_match = re.match(r"^\s+-\s+(.*)$", line)
        if list_match and active_list:
            current = metadata.setdefault(active_list, [])
            if isinstance(current, list):
                current.append(parse_scalar(list_match.group(1)))
            continue
        key_match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if not key_match:
            active_list = None
            continue
        key, raw_value = key_match.groups()
        raw_value = raw_value or ""
        if raw_value.strip():
            metadata[key] = parse_scalar(raw_value)
            active_list = None
        else:
            metadata[key] = []
            active_list = key

    return metadata, "".join(lines[closing_index + 1 :]), closing_index + 2


def split_h2_sections(body: str, body_start_line: int) -> list[Section]:
    """Return exact H2 sections outside fenced code, preserving duplicates."""
    lines = body.splitlines()
    headings: list[tuple[str, int]] = []
    fence_char: str | None = None
    for index, line in enumerate(lines):
        fence = re.match(r"^(`{3,}|~{3,})", line)
        if fence:
            marker = fence.group(1)[0]
            if fence_char is None:
                fence_char = marker
            elif fence_char == marker:
                fence_char = None
            continue
        if fence_char is None:
            heading = re.fullmatch(r"^##(?!#)[ \t]+(.+?)[ \t]*$", line)
            if heading:
                headings.append((heading.group(1).strip(), index))

    sections: list[Section] = []
    for position, (title, heading_index) in enumerate(headings):
        content_start = heading_index + 1
        content_end = (
            headings[position + 1][1] if position + 1 < len(headings) else len(lines)
        )
        content = "\n".join(lines[content_start:content_end]).strip()
        start_line = body_start_line + content_start
        end_line = body_start_line + max(content_start, content_end - 1)
        sections.append(Section(title, content, start_line, end_line))
    return sections


def estimate_tokens(text: str) -> int:
    ascii_chars = sum(1 for char in text if ord(char) < 128)
    non_ascii_chars = len(text) - ascii_chars
    return max(1, (ascii_chars + 1) // 4 + (non_ascii_chars + 1) // 2)


def safe_source_path(project_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        raise ValueError(f"target must be relative to the project root: {value}")
    candidate = project_root / path
    if candidate.is_symlink():
        raise ValueError(f"target must not be a symbolic link: {value}")
    resolved = candidate.resolve()
    if not resolved.is_relative_to(project_root):
        raise ValueError(f"target escapes the project root: {value}")
    if not resolved.is_file():
        raise ValueError(f"target is not a regular file: {value}")
    if resolved.suffix.lower() != ".md":
        raise ValueError(f"target must be Markdown: {value}")
    return resolved


def discover_outline_paths(project_root: Path) -> list[Path]:
    paths: list[Path] = []
    for dirname in ("plot", "outlines"):
        directory = project_root / dirname
        if directory.is_symlink():
            raise ValueError(f"source directory must not be a symbolic link: {dirname}")
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            if path.name.startswith("_"):
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(project_root):
                raise ValueError(
                    f"discovered source must not be a symbolic link: "
                    f"{path.relative_to(project_root)}"
                )
            if path.is_file():
                paths.append(path)
    return paths


def discover_chapter_paths(project_root: Path) -> list[Path]:
    directory = project_root / "chapters"
    if directory.is_symlink():
        raise ValueError("source directory must not be a symbolic link: chapters")
    if not directory.is_dir():
        return []
    paths: list[Path] = []
    for path in sorted(directory.glob("*.md")):
        if not CHAPTER_RE.fullmatch(path.name):
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(project_root):
            raise ValueError(
                f"discovered source must not be a symbolic link: "
                f"{path.relative_to(project_root)}"
            )
        if path.is_file():
            paths.append(path)
    return paths


def select_paths(
    project_root: Path,
    mode: str,
    targets: list[str],
    chapter_numbers: list[int],
) -> list[Path]:
    if targets:
        paths = [safe_source_path(project_root, target) for target in targets]
    elif mode == "outline":
        paths = discover_outline_paths(project_root)
    else:
        paths = discover_chapter_paths(project_root)

    if mode == "chapter" and not targets and not chapter_numbers:
        raise ValueError("chapter mode requires --chapter or --target")
    if mode == "regression" and not targets and not chapter_numbers:
        raise ValueError("regression mode requires --chapter or --target")
    if mode == "outline" and chapter_numbers:
        raise ValueError("outline mode does not accept --chapter")
    if mode == "manuscript" and (targets or chapter_numbers):
        raise ValueError("manuscript mode always inventories every numbered chapter")

    if targets and mode == "outline":
        allowed_directories = {
            project_root / "plot",
            project_root / "outlines",
        }
        invalid = [
            path.relative_to(project_root).as_posix()
            for path in paths
            if path.parent not in allowed_directories
        ]
        if invalid:
            raise ValueError(
                "outline targets must be direct Markdown files under plot/ or outlines/: "
                + ", ".join(invalid)
            )
    if targets and mode in {"chapter", "regression"}:
        invalid = [
            path.relative_to(project_root).as_posix()
            for path in paths
            if path.parent != project_root / "chapters"
            or not CHAPTER_RE.fullmatch(path.name)
        ]
        if invalid:
            raise ValueError(
                f"{mode} targets must be numbered Markdown files under chapters/: "
                + ", ".join(invalid)
            )

    if chapter_numbers:
        wanted = set(chapter_numbers)
        paths = [
            path
            for path in paths
            if (match := CHAPTER_RE.fullmatch(path.name)) and int(match.group(1)) in wanted
        ]
        found = {int(CHAPTER_RE.fullmatch(path.name).group(1)) for path in paths}
        missing = sorted(wanted - found)
        if missing:
            raise ValueError(
                "chapter numbers not found: " + ", ".join(str(number) for number in missing)
            )

    if not paths:
        raise ValueError(f"no review sources found for {mode} mode")
    return sorted(set(paths))


def title_from_body(body: str, fallback: str) -> str:
    for line in body.splitlines():
        match = re.fullmatch(r"^#(?!#)\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return fallback


def unit_for_path(project_root: Path, path: Path, mode: str) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    metadata, body, body_start_line = parse_frontmatter(text)
    relative_path = path.relative_to(project_root).as_posix()
    match = CHAPTER_RE.fullmatch(path.name)
    is_chapter = path.parent == project_root / "chapters" and match is not None
    issues: list[str] = []

    if is_chapter:
        filename_number = int(match.group(1))
        metadata_number = metadata.get("number", filename_number)
        try:
            number = int(metadata_number)
        except (TypeError, ValueError):
            number = filename_number
            issues.append("frontmatter number is invalid")
        if number != filename_number:
            issues.append("frontmatter number does not match the filename")

        sections = split_h2_sections(body, body_start_line)
        section_titles = [section.title for section in sections]
        if section_titles != ["Synopsis", "Draft", "Revision Notes"]:
            issues.append(
                "chapter H2 sections must be exactly Synopsis, Draft, then Revision Notes"
            )
        draft_sections = [
            section
            for section in sections
            if section.title == "Draft"
        ]
        if len(draft_sections) != 1:
            issues.append(f"expected one case-sensitive Draft section, found {len(draft_sections)}")
            review_text = ""
            start_line = None
            end_line = None
        else:
            draft = draft_sections[0]
            review_text = draft.content
            start_line = draft.start_line
            end_line = draft.end_line
            if not review_text:
                issues.append("Draft section is empty")
        review_section = "Draft"
        kind = "chapter"
    else:
        number = None
        review_text = body.strip()
        start_line = body_start_line
        end_line = len(text.splitlines())
        review_section = "document"
        kind = str(metadata.get("type") or "outline")
        if mode != "outline":
            issues.append("non-chapter target is valid only for outline review")
        if not review_text:
            issues.append("review document is empty")

    eligible = not issues
    return {
        "path": relative_path,
        "kind": kind,
        "number": number,
        "title": str(
            metadata.get("title")
            or metadata.get("name")
            or title_from_body(body, path.stem)
        ),
        "status": str(metadata.get("status") or ""),
        "review_section": review_section,
        "line_start": start_line,
        "line_end": end_line,
        "characters": len(review_text),
        "estimated_tokens": estimate_tokens(review_text) if review_text else 0,
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "eligible": eligible,
        "issues": issues,
    }


def build_batches(units: Iterable[dict[str, Any]], max_batch_tokens: int) -> list[dict[str, Any]]:
    batches: list[dict[str, Any]] = []
    current_paths: list[str] = []
    current_tokens = 0

    def flush() -> None:
        nonlocal current_paths, current_tokens
        if current_paths:
            batches.append(
                {
                    "index": len(batches) + 1,
                    "paths": current_paths,
                    "estimated_tokens": current_tokens,
                    "oversized": current_tokens > max_batch_tokens,
                }
            )
            current_paths = []
            current_tokens = 0

    for unit in units:
        if not unit["eligible"]:
            continue
        tokens = int(unit["estimated_tokens"])
        if current_paths and current_tokens + tokens > max_batch_tokens:
            flush()
        current_paths.append(str(unit["path"]))
        current_tokens += tokens
        if current_tokens >= max_batch_tokens:
            flush()
    flush()
    return batches


def build_inventory(
    project_root: Path,
    *,
    mode: str,
    targets: list[str],
    chapter_numbers: list[int],
    max_batch_tokens: int,
) -> dict[str, Any]:
    project_root = project_root.expanduser().resolve()
    if not project_root.is_dir():
        raise ValueError(f"project root is not a directory: {project_root}")
    if max_batch_tokens <= 0:
        raise ValueError("--max-batch-tokens must be positive")

    paths = select_paths(project_root, mode, targets, chapter_numbers)
    units = [unit_for_path(project_root, path, mode) for path in paths]
    chapter_numbers_seen: dict[int, list[dict[str, Any]]] = {}
    for unit in units:
        if unit["kind"] == "chapter" and isinstance(unit["number"], int):
            chapter_numbers_seen.setdefault(unit["number"], []).append(unit)
    for number, matching_units in chapter_numbers_seen.items():
        if len(matching_units) < 2:
            continue
        for unit in matching_units:
            unit["issues"].append(f"duplicate chapter number: {number}")
            unit["eligible"] = False

    batches = build_batches(units, max_batch_tokens)
    issues = [
        {"path": unit["path"], "issues": unit["issues"]}
        for unit in units
        if unit["issues"]
    ]
    return {
        "schema_version": 1,
        "mode": mode,
        "source_policy": (
            "Review chapter reader effects from Draft only; this inventory contains no prose."
        ),
        "unit_count": len(units),
        "eligible_unit_count": sum(1 for unit in units if unit["eligible"]),
        "coverage_complete": not issues and bool(units),
        "max_batch_tokens": max_batch_tokens,
        "units": units,
        "batches": batches,
        "issues": issues,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory outline or manuscript review scope without copying prose."
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--mode", choices=MODES, required=True)
    parser.add_argument("--target", action="append", default=[])
    parser.add_argument("--chapter", action="append", type=int, default=[])
    parser.add_argument("--max-batch-tokens", type=int, default=12000)
    parser.add_argument("--output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        inventory = build_inventory(
            Path(args.project_root),
            mode=args.mode,
            targets=args.target,
            chapter_numbers=args.chapter,
            max_batch_tokens=args.max_batch_tokens,
        )
    except (OSError, UnicodeError, ValueError) as error:
        raise SystemExit(f"Review inventory failed: {error}") from error

    rendered = json.dumps(inventory, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        requested_output = Path(args.output).expanduser()
        output_parent = requested_output.parent.resolve()
        if not output_parent.is_dir():
            raise SystemExit("--output parent must be an existing directory")
        output = output_parent / requested_output.name
        project_root = Path(args.project_root).expanduser().resolve()
        if output == project_root or output.is_relative_to(project_root):
            raise SystemExit("--output must remain outside the reviewed project")
        try:
            descriptor = os.open(
                output,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
            )
        except FileExistsError as error:
            raise SystemExit("--output must not already exist") from error
        with os.fdopen(descriptor, "w", encoding="utf-8") as output_file:
            output_file.write(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
