#!/usr/bin/env python3
"""Write an el_empiezo plot markdown file from JSON."""

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
    "scope",
    "status",
    "starts_in",
    "turns_in",
    "pays_off_in",
    "characters",
    "materials",
    "macguffins",
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
        "id": data.get("id") or f"plot-{slug}",
        "type": "plot",
        "title": title,
        "scope": data.get("scope", "novel"),
        "status": data.get("status", "seed"),
        "starts_in": data.get("starts_in", ""),
        "turns_in": data.get("turns_in", []),
        "pays_off_in": data.get("pays_off_in", ""),
        "characters": data.get("characters", []),
        "materials": data.get("materials", []),
        "macguffins": data.get("macguffins", []),
        "created": data.get("created", today),
        "updated": data.get("updated", today),
        "tags": data.get("tags", []),
    }

    expected_id = f"plot-{slug}"
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
            "## Promise",
            "",
            body_text(body.get("promise"), "What does this thread promise the reader?"),
            "",
            "## Pressure",
            "",
            body_text(body.get("pressure"), "What keeps making the problem harder?"),
            "",
            "## Turns",
            "",
            body_text(
                body.get("turns"),
                "- Setup:\n- Complication:\n- Reversal:\n- Payoff:",
            ),
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
    parser.add_argument("--input", required=True, type=Path, help="Plot JSON file")
    parser.add_argument("--project-root", default=".", type=Path)
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    data = load_json(args.input)
    slug, frontmatter = normalize(data)
    output = args.project_root / "plot" / f"{slug}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {output}")

    output.write_text(render_markdown(data, frontmatter), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
