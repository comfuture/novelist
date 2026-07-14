#!/usr/bin/env python3
"""Create or update a compact canonical chapter-state ledger from reviewed JSON."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any


DEFAULT_LEDGER = Path("materials/000.story-ledger.md")
SECTION_PATTERN = re.compile(
    r"(?ms)^## Chapter (?P<number>\d{3})(?: — (?P<title>.*))?\n(?P<body>.*?)(?=^## Chapter \d{3}(?: — .*?)?\n|\Z)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--input", type=Path, required=True, help="Reviewed JSON fact card")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_card(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object.")
    chapter = data.get("chapter")
    if not isinstance(chapter, int) or chapter < 1:
        raise ValueError("Input requires a positive integer chapter field.")
    if not str(data.get("summary", "")).strip():
        raise ValueError("Input requires a non-empty summary field.")
    return data


def list_lines(values: Any, empty: str = "- None recorded.") -> list[str]:
    if not values:
        return [empty]
    if not isinstance(values, list):
        values = [values]
    result = []
    for value in values:
        if isinstance(value, dict):
            identifier = value.get("id") or value.get("name") or value.get("fact_id") or "item"
            status = value.get("status")
            description = value.get("description") or value.get("change") or value.get("fact") or ""
            suffix = f" [{status}]" if status else ""
            result.append(f"- {identifier}{suffix}: {description}".rstrip())
        else:
            result.append(f"- {value}")
    return result


def render_section(card: dict[str, Any]) -> str:
    number = card["chapter"]
    title = str(card.get("title", "")).strip()
    heading = f"## Chapter {number:03d}" + (f" — {title}" if title else "")
    fields = (
        ("Summary", [str(card["summary"]).strip()]),
        ("Canon Facts", list_lines(card.get("canon_facts"))),
        ("Character And Relationship Changes", list_lines(card.get("state_changes"))),
        ("Timeline And Location Changes", list_lines(card.get("timeline_changes"))),
        ("Reveals And Knowledge Changes", list_lines(card.get("knowledge_changes"))),
        ("MacGuffin And Clue Changes", list_lines(card.get("macguffin_changes"))),
        ("Open Threads", list_lines(card.get("open_threads"))),
        ("Resolved Threads", list_lines(card.get("resolved_threads"))),
        ("Contradictions Or Uncertainties", list_lines(card.get("uncertainties"))),
    )
    lines = [heading, ""]
    for label, values in fields:
        lines.extend([f"### {label}", "", *values, ""])
    return "\n".join(lines).rstrip() + "\n"


def initial_document(today: str) -> str:
    return (
        "---\n"
        "id: material-story-ledger\n"
        "type: material\n"
        "title: \"Story Continuity Ledger\"\n"
        "category: continuity-ledger\n"
        "status: draft\n"
        "canonical: true\n"
        "related_characters: []\n"
        "related_macguffins: []\n"
        "plot_threads: []\n"
        "used_in_chapters: []\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        "tags: [continuity, story-state]\n"
        "---\n"
        "# Story Continuity Ledger\n\n"
        "This ledger records reviewed chapter outcomes. Canonical source files remain authoritative when conflicts exist.\n\n"
    )


def update_date(text: str, today: str) -> str:
    return re.sub(r"(?m)^updated:\s*.*$", f"updated: {today}", text, count=1)


def replace_section(document: str, section: str, chapter: int) -> str:
    matches = list(SECTION_PATTERN.finditer(document))
    replacement_done = False
    parts: list[str] = []
    cursor = 0
    for match in matches:
        parts.append(document[cursor : match.start()])
        if int(match.group("number")) == chapter:
            parts.append(section.rstrip() + "\n\n")
            replacement_done = True
        else:
            parts.append(match.group(0).rstrip() + "\n\n")
        cursor = match.end()
    parts.append(document[cursor:])
    result = "".join(parts).rstrip() + "\n"
    if replacement_done:
        return result
    return result.rstrip() + "\n\n" + section


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, path)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    ledger = args.ledger if args.ledger.is_absolute() else root / args.ledger
    try:
        card = load_card(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Cannot load fact card: {exc}", file=sys.stderr)
        return 2
    today = date.today().isoformat()
    document = ledger.read_text(encoding="utf-8") if ledger.exists() else initial_document(today)
    updated = replace_section(update_date(document, today), render_section(card), card["chapter"])
    if args.dry_run:
        sys.stdout.write(updated)
    else:
        atomic_write(ledger, updated)
        print(f"Updated {ledger.relative_to(root) if ledger.is_relative_to(root) else ledger}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
