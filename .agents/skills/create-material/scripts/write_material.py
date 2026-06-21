#!/usr/bin/env python3
"""Write an el_empiezo story material markdown file from JSON."""

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
    "title",
    "category",
    "status",
    "source",
    "canonical",
    "related_characters",
    "related_macguffins",
    "plot_threads",
    "used_in_chapters",
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


def body_text(value: Any, fallback: str) -> str:
    if isinstance(value, str):
        return value.strip() or fallback
    if isinstance(value, list):
        lines = [str(item).strip() for item in value if str(item).strip()]
        if lines:
            return "\n".join(f"- {line}" for line in lines)
    return fallback


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

    title = str(data.get("title", "")).strip()
    if not title:
        raise SystemExit("Missing required field: title")

    today = dt.date.today().isoformat()
    frontmatter = {
        "id": data.get("id") or f"material-{slug}",
        "type": "material",
        "title": title,
        "category": data.get("category", "scene-seed"),
        "status": data.get("status", "seed"),
        "source": data.get("source", ""),
        "canonical": data.get("canonical", False),
        "related_characters": data.get("related_characters", []),
        "related_macguffins": data.get("related_macguffins", []),
        "plot_threads": data.get("plot_threads", []),
        "used_in_chapters": data.get("used_in_chapters", []),
        "created": data.get("created", today),
        "updated": data.get("updated", today),
        "tags": data.get("tags", []),
    }

    expected_id = f"material-{slug}"
    if frontmatter["id"] != expected_id:
        raise SystemExit(f"id must be {expected_id!r} for slug {slug!r}")
    return slug, frontmatter


def render_body(data: dict[str, Any]) -> str:
    body = data.get("body") or {}
    if not isinstance(body, dict):
        raise TypeError("body must be an object when provided")
    return "\n".join(
        [
            f"# {data['title']}",
            "",
            "## Idea",
            "",
            body_text(body.get("idea"), "Capture the raw material here."),
            "",
            "## Story Use",
            "",
            body_text(body.get("story_use"), "How might this become a scene, motif, object, line, conflict, or reveal?"),
            "",
            "## Notes",
            "",
            body_text(body.get("notes"), "Keep references, constraints, and questions here."),
            "",
        ]
    )


def render_markdown(data: dict[str, Any], frontmatter: dict[str, Any]) -> str:
    lines = ["---"]
    for key in FRONTMATTER_ORDER:
        lines.append(f"{key}: {yaml_scalar(frontmatter[key])}")
    lines.extend(["---", render_body(data)])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="Material JSON file")
    parser.add_argument("--project-root", default=".", type=Path)
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    data = load_json(args.input)
    slug, frontmatter = normalize(data)
    output = args.project_root / "materials" / f"{slug}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {output}")

    output.write_text(render_markdown(data, frontmatter), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
