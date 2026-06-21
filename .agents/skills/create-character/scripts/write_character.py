#!/usr/bin/env python3
"""Write a novel character markdown file from JSON."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

FRONTMATTER_ORDER = [
    "id",
    "type",
    "name",
    "original_name",
    "korean_reading",
    "name_language",
    "name_context",
    "aliases",
    "role",
    "status",
    "age",
    "gender",
    "pronouns",
    "first_appearance",
    "last_seen",
    "relationships",
    "wants",
    "needs",
    "conflicts",
    "secrets",
    "related_materials",
    "related_macguffins",
    "plot_threads",
    "created",
    "updated",
    "tags",
]


def yaml_scalar(value: Any) -> str:
    if value is None:
        return '""'
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        if not value:
            return "[]"
        return "[" + ", ".join(yaml_scalar(item) for item in value) + "]"
    if isinstance(value, dict):
        raise TypeError("Nested objects are not supported in frontmatter fields")
    return json.dumps(str(value), ensure_ascii=False)


def body_list(items: Any, fallback: str = "") -> str:
    if isinstance(items, str):
        return items.strip() or fallback
    if isinstance(items, list):
        lines = [str(item).strip() for item in items if str(item).strip()]
        if lines:
            return "\n".join(f"- {line}" for line in lines)
    return fallback


def render_body(data: dict[str, Any]) -> str:
    body = data.get("body") or {}
    if not isinstance(body, dict):
        raise TypeError("body must be an object when provided")

    name = str(data["name"]).strip()
    function = body_list(body.get("function"), "What does this character do for the story?")
    surface = body_list(
        body.get("surface"),
        "- Public identity:\n- Occupation or social role:\n- Visible habits:",
    )
    interior = body_list(
        body.get("interior"),
        "- Desire:\n- Fear:\n- Contradiction:\n- Private wound:",
    )
    relationships = body_list(
        body.get("relationships") or data.get("relationships"),
        "List important relationships and how each one changes.",
    )
    continuity = body_list(
        body.get("continuity"),
        "Track facts that must stay consistent across chapters.",
    )

    return "\n".join(
        [
            f"# {name}",
            "",
            "## Function",
            "",
            function,
            "",
            "## Surface",
            "",
            surface,
            "",
            "## Interior",
            "",
            interior,
            "",
            "## Relationships",
            "",
            relationships,
            "",
            "## Continuity",
            "",
            continuity,
            "",
        ]
    )


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("Input JSON must be an object")
    return data


def normalize(data: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    slug = str(data.get("slug", "")).strip()
    if not slug:
        raise SystemExit("Missing required field: slug")
    if not SLUG_RE.fullmatch(slug):
        raise SystemExit(
            "Invalid slug. Use lowercase ASCII letters, digits, and hyphens only."
        )

    name = str(data.get("name", "")).strip()
    if not name:
        raise SystemExit("Missing required field: name")

    today = dt.date.today().isoformat()
    frontmatter: dict[str, Any] = {
        "id": data.get("id") or f"char-{slug}",
        "type": "character",
        "name": name,
        "original_name": data.get("original_name", name),
        "korean_reading": data.get("korean_reading", name),
        "name_language": data.get("name_language", "ko"),
        "name_context": data.get("name_context", ""),
        "aliases": data.get("aliases", []),
        "role": data.get("role", ""),
        "status": data.get("status", "seed"),
        "age": data.get("age", ""),
        "gender": data.get("gender", ""),
        "pronouns": data.get("pronouns", ""),
        "first_appearance": data.get("first_appearance", ""),
        "last_seen": data.get("last_seen", ""),
        "relationships": data.get("relationships", []),
        "wants": data.get("wants", []),
        "needs": data.get("needs", []),
        "conflicts": data.get("conflicts", []),
        "secrets": data.get("secrets", []),
        "related_materials": data.get("related_materials", []),
        "related_macguffins": data.get("related_macguffins", []),
        "plot_threads": data.get("plot_threads", []),
        "created": data.get("created", today),
        "updated": data.get("updated", today),
        "tags": data.get("tags", []),
    }

    expected_id = f"char-{slug}"
    if frontmatter["id"] != expected_id:
        raise SystemExit(f"id must be {expected_id!r} for slug {slug!r}")

    return slug, frontmatter


def render_markdown(data: dict[str, Any], frontmatter: dict[str, Any]) -> str:
    lines = ["---"]
    for key in FRONTMATTER_ORDER:
        lines.append(f"{key}: {yaml_scalar(frontmatter[key])}")
    lines.extend(["---", render_body(data)])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="Character JSON file")
    parser.add_argument("--project-root", default=".", type=Path)
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    data = load_json(args.input)
    slug, frontmatter = normalize(data)
    output = args.project_root / "characters" / f"{slug}.md"
    output.parent.mkdir(parents=True, exist_ok=True)

    if output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {output}")

    markdown = render_markdown(data, frontmatter)
    output.write_text(markdown, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
