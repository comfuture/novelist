#!/usr/bin/env python3
"""Build a compact, source-attributed context pack for the next chapter."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from story_io import Record, clip_text, dump_json, estimate_tokens, linked_ids, load_records


CORE_PATHS = {
    "project.md": 170,
    "style/000.style-guide.md": 160,
    "plot/000.master-plot.md": 175,
    "outlines/000.master-outline.md": 155,
    "materials/000.story-ledger.md": 1000,
}

FOCUS_SECTIONS = {
    "function",
    "interior",
    "relationships",
    "continuity",
    "story use",
    "truth",
    "reveal plan",
    "pressure",
    "turns",
    "purpose",
    "beats",
    "continuity notes",
    "story pressure",
    "voice",
    "point of view",
    "tense",
    "terms",
    "revision preferences",
    "open questions",
    "continuity watchlist",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--chapter", type=int, required=True, help="Chapter number being prepared")
    parser.add_argument("--recent", type=int, default=3, help="Number of prior chapters to include")
    parser.add_argument("--query", default="", help="Optional scene, entity, location, or theme focus")
    parser.add_argument("--max-tokens", type=int, default=6000)
    parser.add_argument("--output-language", default="auto")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def language_contract(records: list[Record], requested: str) -> str:
    if requested != "auto":
        return requested
    project = next((record for record in records if record.relpath == "project.md"), None)
    if project and project.metadata.get("language"):
        return str(project.metadata["language"])
    style = next((record for record in records if record.kind == "style_guide"), None)
    if style and style.metadata.get("language"):
        return str(style.metadata["language"])
    return "the language used by the recent manuscript"


def query_terms(query: str) -> set[str]:
    return {term.casefold() for term in re.findall(r"[\w-]{2,}", query, flags=re.UNICODE)}


def score_record(
    record: Record,
    target: int,
    recent_numbers: set[int],
    explicit_ids: set[str],
    terms: set[str],
) -> int:
    score = CORE_PATHS.get(record.relpath, 0)
    if record.identifier in explicit_ids:
        score += 700
    if record.chapter_number == target and record.kind == "outline":
        score += 1200
    if record.kind == "chapter" and record.chapter_number in recent_numbers:
        score += 900 + (record.chapter_number or 0)
    if record.kind in {"character", "macguffin", "plot", "world"}:
        score += 12
    haystack = " ".join(
        [record.identifier, record.label, str(record.metadata.get("tags", "")), record.body[:5000]]
    ).casefold()
    score += min(40, sum(8 for term in terms if term in haystack))
    if record.metadata.get("status") in {"final", "revision", "draft"}:
        score += 5
    return score


def selected_sections(record: Record) -> list[tuple[str, str]]:
    if record.kind == "chapter":
        chosen: list[tuple[str, str]] = []
        for key in ("synopsis", "revision notes"):
            value = record.sections.get(key)
            if value:
                chosen.append((key.title(), value))
        draft = record.sections.get("draft") or record.body
        if draft:
            chosen.append(("Closing Excerpt", clip_text(draft, 1400, keep_tail=True)))
        return chosen
    if record.relpath == "materials/000.story-ledger.md":
        return [("Recent Story Ledger", clip_text(record.body, 5000, keep_tail=True))]
    chosen = []
    for key, value in record.sections.items():
        if value and (key in FOCUS_SECTIONS or record.relpath in CORE_PATHS):
            chosen.append((key.title(), value))
    if not chosen and record.body:
        chosen.append(("Excerpt", record.body))
    return chosen


def compact_record(record: Record, char_limit: int) -> dict[str, Any]:
    meta_keys = (
        "id",
        "type",
        "title",
        "name",
        "status",
        "number",
        "pov",
        "timeline",
        "setting",
        "role",
        "scope",
        "characters",
        "materials",
        "macguffins",
        "plot_threads",
        "rules",
        "tags",
    )
    metadata = {key: record.metadata[key] for key in meta_keys if record.metadata.get(key) not in (None, "", [])}
    sections = []
    remaining = max(300, char_limit)
    for heading, value in selected_sections(record):
        excerpt = clip_text(value, min(2400, remaining), keep_tail=heading == "Closing Excerpt")
        if not excerpt:
            continue
        sections.append({"heading": heading, "text": excerpt})
        remaining -= len(excerpt)
        if remaining < 200:
            break
    return {"source": record.relpath, "metadata": metadata, "sections": sections}


def render_markdown(pack: dict[str, Any]) -> str:
    lines = [
        "# Story Context Pack",
        "",
        f"- Target chapter: {pack['target_chapter']:03d}",
        f"- Output language: {pack['output_language']}",
        f"- Estimated tokens: {pack['estimated_tokens']}",
        "- Authority: explicit author direction, then canonical source status and recency; flag conflicts instead of guessing.",
        "",
    ]
    for item in pack["sources"]:
        label = item["metadata"].get("title") or item["metadata"].get("name") or item["metadata"].get("id")
        lines.extend([f"## {label or item['source']}", "", f"Source: `{item['source']}`", ""])
        if item["metadata"]:
            lines.extend(["Metadata:", "```json", dump_json(item["metadata"]), "```", ""])
        for section in item["sections"]:
            lines.extend([f"### {section['heading']}", "", section["text"], ""])
    return "\n".join(lines).rstrip() + "\n"


def render_pack(pack: dict[str, Any], output_format: str) -> str:
    return dump_json(pack) + "\n" if output_format == "json" else render_markdown(pack)


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    records = load_records(root)
    if not records:
        print("No novel source files found.", file=sys.stderr)
        return 2
    if args.max_tokens < 300:
        print("--max-tokens must be at least 300.", file=sys.stderr)
        return 2
    recent_numbers = set(range(max(1, args.chapter - args.recent), args.chapter))
    target_records = [
        record
        for record in records
        if (record.kind == "outline" and record.metadata.get("chapter") == args.chapter)
        or (record.kind == "chapter" and record.chapter_number in recent_numbers)
    ]
    explicit_ids = set().union(*(linked_ids(record) for record in target_records)) if target_records else set()
    terms = query_terms(args.query)
    ranked = sorted(
        ((score_record(record, args.chapter, recent_numbers, explicit_ids, terms), record) for record in records),
        key=lambda pair: (pair[0], pair[1].relpath),
        reverse=True,
    )

    sources: list[dict[str, Any]] = []
    for score, record in ranked:
        if score <= 0:
            continue
        best: dict[str, Any] | None = None
        low, high = 300, 5200
        while low <= high:
            allowance = (low + high) // 2
            item = compact_record(record, allowance)
            candidate = {
                "target_chapter": args.chapter,
                "output_language": language_contract(records, args.output_language),
                "query": args.query,
                "sources": [*sources, item],
                "estimated_tokens": 0,
            }
            if estimate_tokens(render_pack(candidate, args.format)) <= args.max_tokens - 10:
                best = item
                low = allowance + 1
            else:
                high = allowance - 1
        if best and (best["sections"] or best["metadata"]):
            sources.append(best)

    pack: dict[str, Any] = {
        "target_chapter": args.chapter,
        "output_language": language_contract(records, args.output_language),
        "query": args.query,
        "sources": sources,
        "estimated_tokens": 0,
    }
    for _ in range(2):
        pack["estimated_tokens"] = estimate_tokens(render_pack(pack, args.format))
    output = render_pack(pack, args.format)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
