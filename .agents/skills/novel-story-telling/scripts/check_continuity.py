#!/usr/bin/env python3
"""Run deterministic structural continuity checks over the novel sources."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from story_io import ID_PREFIXES, LINK_FIELDS, as_list, dump_json, load_records


REQUIRED = {"id", "type", "status", "tags", "created", "updated"}
VALID_TYPES = {
    "project",
    "documentation",
    "character",
    "material",
    "macguffin",
    "plot",
    "outline",
    "world",
    "style_guide",
    "chapter",
    "publishing_note",
}
VALID_STATUSES = {"seed", "outline", "draft", "revision", "final", "archived"}
CHAPTER_NAME = re.compile(r"^(\d{3})\.([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CHAPTER_REQUIRED = {
    "id",
    "type",
    "number",
    "title",
    "slug",
    "status",
    "pov",
    "timeline",
    "setting",
    "word_target",
    "characters",
    "materials",
    "macguffins",
    "plot_threads",
    "outline",
    "published",
    "created",
    "updated",
    "tags",
}
CHAPTER_LIST_FIELDS = ("characters", "materials", "macguffins", "plot_threads", "tags")
CHAPTER_STRING_FIELDS = ("id", "type", "title", "slug", "status", "pov", "timeline", "setting", "outline")
CHAPTER_SECTIONS = ("Synopsis", "Draft", "Revision Notes")
TEMPLATE_PLACEHOLDERS = (
    "Copy this template to a filename like",
    "One or two paragraphs describing what changes in this chapter.",
    "Write the chapter prose here.",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as a failing exit status")
    return parser.parse_args()


def issue(level: str, code: str, path: str, message: str) -> dict[str, str]:
    return {"level": level, "code": code, "source": path, "message": message}


def audit(root: Path) -> dict[str, Any]:
    records = load_records(root)
    issues: list[dict[str, str]] = []
    chapters_dir = root / "chapters"
    if chapters_dir.is_dir():
        for path in sorted(chapters_dir.glob("**/*.md")):
            if path.parent != chapters_dir:
                issues.append(
                    issue(
                        "error",
                        "nested-chapter",
                        path.relative_to(root).as_posix(),
                        "Chapter Markdown files must live directly under chapters/.",
                    )
                )
    ids = [record.identifier for record in records if record.identifier]
    id_set = set(ids)
    for identifier, count in Counter(ids).items():
        if count > 1:
            paths = [record.relpath for record in records if record.identifier == identifier]
            issues.append(issue("error", "duplicate-id", ", ".join(paths), f"ID {identifier!r} appears {count} times."))

    chapter_numbers: list[int] = []
    for record in records:
        meta = record.metadata
        missing = sorted(REQUIRED - set(meta))
        if not (meta.get("title") or meta.get("name")):
            missing.append("title-or-name")
        if missing:
            issues.append(issue("error", "missing-frontmatter", record.relpath, f"Missing: {', '.join(missing)}."))
        if meta.get("type") not in VALID_TYPES:
            issues.append(issue("error", "invalid-type", record.relpath, f"Invalid type: {meta.get('type')!r}."))
        if meta.get("status") not in VALID_STATUSES:
            issues.append(issue("error", "invalid-status", record.relpath, f"Invalid status: {meta.get('status')!r}."))
        for date_field in ("created", "updated"):
            if date_field in meta and not DATE.fullmatch(str(meta[date_field])):
                issues.append(issue("error", "invalid-date", record.relpath, f"{date_field} must use YYYY-MM-DD."))
            elif date_field in meta:
                try:
                    date.fromisoformat(str(meta[date_field]))
                except ValueError:
                    issues.append(issue("error", "invalid-date", record.relpath, f"{date_field} is not a real date."))

        is_chapter_path = record.path.parent.name == "chapters"
        if is_chapter_path and record.kind != "chapter":
            issues.append(issue("error", "chapter-type", record.relpath, "Files in chapters/ must use type: chapter."))

        if is_chapter_path:
            chapter_missing = sorted(CHAPTER_REQUIRED - set(meta))
            if chapter_missing:
                issues.append(
                    issue("error", "chapter-frontmatter", record.relpath, f"Missing: {', '.join(chapter_missing)}.")
                )
            match = CHAPTER_NAME.fullmatch(record.path.name)
            if not match:
                issues.append(issue("error", "chapter-filename", record.relpath, "Filename does not match NNN.ascii-slug.md."))
            else:
                number = int(match.group(1))
                slug = match.group(2)
                chapter_numbers.append(number)
                if record.chapter_number != number:
                    issues.append(issue("error", "chapter-number", record.relpath, "Frontmatter number does not match filename."))
                if meta.get("id") != f"chapter-{number:03d}":
                    issues.append(issue("error", "chapter-id", record.relpath, f"Expected id chapter-{number:03d}."))
                if meta.get("slug") != slug:
                    issues.append(issue("error", "chapter-slug", record.relpath, f"Expected slug {slug!r}."))

            for field in CHAPTER_LIST_FIELDS:
                if field in meta and not isinstance(meta[field], list):
                    issues.append(issue("error", "chapter-list-field", record.relpath, f"{field} must be a YAML array."))
            for field in CHAPTER_STRING_FIELDS:
                if field in meta and not isinstance(meta[field], str):
                    issues.append(issue("error", "chapter-string-field", record.relpath, f"{field} must be a string."))
            chapter_number = meta.get("number")
            if "number" in meta and (
                isinstance(chapter_number, bool) or not isinstance(chapter_number, int) or not 1 <= chapter_number <= 999
            ):
                issues.append(issue("error", "chapter-number-type", record.relpath, "number must be an integer from 1 through 999."))
            word_target = meta.get("word_target")
            if "word_target" in meta and (
                isinstance(word_target, bool) or not isinstance(word_target, int) or word_target <= 0
            ):
                issues.append(issue("error", "chapter-word-target", record.relpath, "word_target must be a positive integer."))
            if "published" in meta and not isinstance(meta.get("published"), bool):
                issues.append(issue("error", "chapter-published", record.relpath, "published must be a boolean."))

            headings = re.findall(r"^(#{1,6})\s+(.+?)\s*$", record.body, flags=re.MULTILINE)
            h1_titles = [title for level, title in headings if level == "#"]
            if len(h1_titles) != 1:
                issues.append(issue("error", "chapter-h1", record.relpath, "Chapter body must contain exactly one H1."))
            elif h1_titles[0] != str(meta.get("title", "")):
                issues.append(issue("error", "chapter-title", record.relpath, "H1 must exactly match frontmatter title."))
            first_line = record.body.splitlines()[0].strip() if record.body else ""
            if first_line != f"# {meta.get('title', '')}":
                issues.append(issue("error", "chapter-first-heading", record.relpath, "The first body line must be the title H1."))
            h2_titles = [title for level, title in headings if level == "##"]
            for section in CHAPTER_SECTIONS:
                if h2_titles.count(section) != 1:
                    issues.append(
                        issue("error", "chapter-section", record.relpath, f"Chapter must contain exactly one ## {section} section.")
                    )
            if all(h2_titles.count(section) == 1 for section in CHAPTER_SECTIONS):
                positions = [h2_titles.index(section) for section in CHAPTER_SECTIONS]
                if positions != sorted(positions):
                    issues.append(
                        issue(
                            "error",
                            "chapter-section-order",
                            record.relpath,
                            "Required sections must appear as Synopsis, Draft, then Revision Notes.",
                        )
                    )
            if meta.get("status") in {"draft", "revision", "final"} and not record.sections.get("synopsis", "").strip():
                issues.append(issue("error", "chapter-synopsis", record.relpath, "Synopsis section must not be empty."))
            if meta.get("status") in {"draft", "revision", "final"} and not record.sections.get("draft", "").strip():
                issues.append(issue("error", "chapter-draft", record.relpath, "Draft section must not be empty."))
            for placeholder in TEMPLATE_PLACEHOLDERS:
                if placeholder in record.body:
                    issues.append(
                        issue("error", "chapter-placeholder", record.relpath, f"Remove template placeholder: {placeholder!r}.")
                    )

        for field in LINK_FIELDS:
            for value in as_list(meta.get(field)):
                reference = str(value).strip()
                if reference.startswith(ID_PREFIXES) and reference not in id_set:
                    issues.append(issue("warning", "dangling-reference", record.relpath, f"{field} references missing ID {reference!r}."))

    if chapter_numbers:
        for number, count in Counter(chapter_numbers).items():
            if count > 1:
                issues.append(
                    issue("error", "duplicate-chapter-number", "chapters/", f"Chapter number {number:03d} appears {count} times.")
                )
        ordered = sorted(set(chapter_numbers))
        expected = set(range(ordered[0], ordered[-1] + 1))
        for number in sorted(expected - set(ordered)):
            issues.append(issue("warning", "chapter-gap", "chapters/", f"Chapter {number:03d} is missing."))

    return {
        "project_root": str(root),
        "files_checked": len(records),
        "errors": sum(item["level"] == "error" for item in issues),
        "warnings": sum(item["level"] == "warning" for item in issues),
        "issues": issues,
        "semantic_review": [
            "Compare the proposed chapter against every linked source's Continuity section.",
            "Verify character knowledge, possessions, injuries, relationships, and location at scene entry and exit.",
            "Verify setup, clue, secret, MacGuffin, and plot-thread states before changing or paying them off.",
            "Verify timeline order, elapsed time, travel constraints, and world-rule costs.",
            "Treat silence as uncertainty; do not convert absent evidence into canon.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Continuity Audit",
        "",
        f"- Files checked: {report['files_checked']}",
        f"- Errors: {report['errors']}",
        f"- Warnings: {report['warnings']}",
        "",
        "## Structural Findings",
        "",
    ]
    if report["issues"]:
        for item in report["issues"]:
            lines.append(f"- [{item['level'].upper()}] `{item['code']}` in `{item['source']}`: {item['message']}")
    else:
        lines.append("- No structural continuity issues found.")
    lines.extend(["", "## Semantic Review Gate", ""])
    lines.extend(f"- {entry}" for entry in report["semantic_review"])
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    report = audit(args.project_root.resolve())
    output = dump_json(report) + "\n" if args.format == "json" else render_markdown(report)
    sys.stdout.write(output)
    if report["errors"] or (args.strict and report["warnings"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
