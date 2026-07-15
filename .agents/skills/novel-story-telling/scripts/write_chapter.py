#!/usr/bin/env python3
"""Create one template-conformant chapter file from reviewed JSON input."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any, NoReturn


SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VALID_STATUSES = {"outline", "draft", "revision", "final"}
LIST_FIELDS = ("characters", "materials", "macguffins", "plot_threads", "tags")
STRING_FIELDS = ("pov", "timeline", "setting", "outline", "revision_notes")
ALLOWED_FIELDS = {
    "number",
    "title",
    "slug",
    "status",
    "word_target",
    "created",
    "updated",
    "published",
    "synopsis",
    "draft",
    *LIST_FIELDS,
    *STRING_FIELDS,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--input", type=Path, required=True, help="Reviewed UTF-8 JSON chapter payload")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print Markdown without writing")
    return parser.parse_args()


def fail(message: str) -> NoReturn:
    raise ValueError(message)


def require_text(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(f"{key} must be a non-empty string")
    return value.strip()


def optional_text(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key, "")
    if not isinstance(value, str):
        fail(f"{key} must be a string")
    return value.strip()


def string_list(payload: dict[str, Any], key: str) -> list[str]:
    value = payload.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        fail(f"{key} must be an array of non-empty strings")
    return [item.strip() for item in value]


def yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_list(key: str, values: list[str]) -> list[str]:
    if not values:
        return [f"{key}: []"]
    return [f"{key}:", *(f"  - {yaml_scalar(value)}" for value in values)]


def validate_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        fail("input must be a JSON object")
    unknown = sorted(set(payload) - ALLOWED_FIELDS)
    if unknown:
        fail(f"unknown input fields: {', '.join(unknown)}")

    number = payload.get("number")
    if isinstance(number, bool) or not isinstance(number, int) or not 1 <= number <= 999:
        fail("number must be an integer from 1 through 999")

    title = require_text(payload, "title")
    slug = require_text(payload, "slug")
    if not SLUG.fullmatch(slug):
        fail("slug must contain lowercase ASCII letters or digits separated by single hyphens")

    status = payload.get("status", "draft")
    if status not in VALID_STATUSES:
        fail(f"status must be one of: {', '.join(sorted(VALID_STATUSES))}")

    word_target = payload.get("word_target", 2500)
    if isinstance(word_target, bool) or not isinstance(word_target, int) or word_target <= 0:
        fail("word_target must be a positive integer")

    created = payload.get("created", date.today().isoformat())
    updated = payload.get("updated", created)
    for key, value in (("created", created), ("updated", updated)):
        if not isinstance(value, str) or not DATE.fullmatch(value):
            fail(f"{key} must use YYYY-MM-DD")
        try:
            date.fromisoformat(value)
        except ValueError:
            fail(f"{key} must be a real calendar date")

    published = payload.get("published", False)
    if not isinstance(published, bool):
        fail("published must be a boolean")
    if published:
        fail("a newly created chapter must use published: false")
    if updated < created:
        fail("updated must not be earlier than created")

    return {
        "number": number,
        "title": title,
        "slug": slug,
        "status": status,
        "word_target": word_target,
        "created": created,
        "updated": updated,
        "published": published,
        "synopsis": require_text(payload, "synopsis"),
        "draft": require_text(payload, "draft"),
        **{key: optional_text(payload, key) for key in STRING_FIELDS},
        **{key: string_list(payload, key) for key in LIST_FIELDS},
    }


def render_chapter(data: dict[str, Any]) -> str:
    number = data["number"]
    lines = [
        "---",
        f"id: chapter-{number:03d}",
        "type: chapter",
        f"number: {number}",
        f"title: {yaml_scalar(data['title'])}",
        f"slug: {data['slug']}",
        f"status: {data['status']}",
        f"pov: {yaml_scalar(data['pov'])}",
        f"timeline: {yaml_scalar(data['timeline'])}",
        f"setting: {yaml_scalar(data['setting'])}",
        f"word_target: {data['word_target']}",
    ]
    for field in ("characters", "materials", "macguffins", "plot_threads"):
        lines.extend(yaml_list(field, data[field]))
    lines.extend(
        [
            f"outline: {yaml_scalar(data['outline'])}",
            f"published: {'true' if data['published'] else 'false'}",
            f"created: {data['created']}",
            f"updated: {data['updated']}",
        ]
    )
    lines.extend(yaml_list("tags", data["tags"]))
    lines.extend(
        [
            "---",
            f"# {data['title']}",
            "",
            "## Synopsis",
            "",
            data["synopsis"],
            "",
            "## Draft",
            "",
            data["draft"],
            "",
            "## Revision Notes",
            "",
        ]
    )
    if data["revision_notes"]:
        lines.append(data["revision_notes"])
        lines.append("")
    return "\n".join(lines)


def ensure_available(chapters: Path, number: int, target: Path) -> None:
    conflicts = sorted(chapters.glob(f"{number:03d}.*.md"))
    if conflicts:
        names = ", ".join(path.name for path in conflicts)
        fail(f"chapter number {number:03d} already exists: {names}; revise the existing file instead")
    if target.exists():
        fail(f"refusing to overwrite existing file: {target}")


def atomic_write(target: Path, content: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        os.chmod(temporary, 0o644)
        os.replace(temporary, target)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        data = validate_payload(payload)
        root = args.project_root.resolve()
        chapters = root / "chapters"
        target = chapters / f"{data['number']:03d}.{data['slug']}.md"
        ensure_available(chapters, data["number"], target)
        content = render_chapter(data)
        if args.dry_run:
            sys.stdout.write(content)
        else:
            atomic_write(target, content)
            print(target.relative_to(root).as_posix())
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
