#!/usr/bin/env python3
"""Shared, dependency-free readers for the novel project's Markdown sources."""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


SOURCE_FILES = ("project.md",)
SOURCE_DIRECTORIES = (
    "characters",
    "materials",
    "macguffins",
    "plot",
    "outlines",
    "world",
    "style",
    "chapters",
)

LINK_FIELDS = {
    "characters",
    "major_characters",
    "related_characters",
    "materials",
    "related_materials",
    "macguffins",
    "related_macguffins",
    "plot_threads",
    "related_outlines",
    "outline",
    "source_plot",
    "holder",
    "introduced_in",
    "revealed_in",
    "resolved_in",
    "starts_in",
    "turns_in",
    "pays_off_in",
    "first_appearance",
    "last_seen",
    "used_in_chapters",
}

ID_PREFIXES = (
    "chapter-",
    "char-",
    "material-",
    "macguffin-",
    "plot-",
    "outline-",
    "world-",
    "style-",
)


@dataclass(frozen=True)
class Record:
    path: Path
    relpath: str
    metadata: dict[str, Any]
    body: str
    sections: dict[str, str]

    @property
    def identifier(self) -> str:
        value = self.metadata.get("id", "")
        return str(value).strip()

    @property
    def kind(self) -> str:
        value = self.metadata.get("type", "")
        return str(value).strip()

    @property
    def label(self) -> str:
        value = self.metadata.get("title") or self.metadata.get("name") or self.identifier
        return str(value).strip()

    @property
    def chapter_number(self) -> int | None:
        value = self.metadata.get("number")
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
        match = re.match(r"^(\d{3})\.", self.path.name)
        return int(match.group(1)) if match else None


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


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    metadata: dict[str, Any] = {}
    active_list: str | None = None
    for raw_line in raw.splitlines():
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
        if raw_value.strip() == "":
            metadata[key] = []
            active_list = key
        else:
            metadata[key] = parse_scalar(raw_value)
            active_list = None
    return metadata, body


def split_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {"_lead": []}
    current = "_lead"
    for line in body.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            current = match.group(2).strip().lower()
            sections.setdefault(current, [])
            continue
        sections[current].append(line)
    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def split_h2_sections(body: str) -> list[tuple[str, str]]:
    """Return exact H2 sections outside fenced code, preserving duplicates."""
    headings: list[tuple[str, int, int]] = []
    fence_char: str | None = None
    offset = 0
    for raw_line in body.splitlines(keepends=True):
        line = raw_line.rstrip("\r\n")
        fence = re.match(r"^(`{3,}|~{3,})", line)
        if fence:
            marker_char = fence.group(1)[0]
            if fence_char is None:
                fence_char = marker_char
            elif fence_char == marker_char:
                fence_char = None
            offset += len(raw_line)
            continue
        if fence_char is None:
            heading = re.fullmatch(r"^##(?!#)[ \t]+(.+?)[ \t]*$", line)
            if heading:
                headings.append((heading.group(1).strip(), offset, offset + len(raw_line)))
        offset += len(raw_line)

    sections: list[tuple[str, str]] = []
    for index, (title, _start, content_start) in enumerate(headings):
        content_end = headings[index + 1][1] if index + 1 < len(headings) else len(body)
        sections.append((title, body[content_start:content_end].strip()))
    return sections


def read_record(path: Path, root: Path) -> Record:
    text = path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(text)
    return Record(
        path=path,
        relpath=path.relative_to(root).as_posix(),
        metadata=metadata,
        body=body.strip(),
        sections=split_sections(body),
    )


def iter_source_paths(root: Path) -> Iterable[Path]:
    for filename in SOURCE_FILES:
        path = root / filename
        if path.is_file():
            yield path
    for dirname in SOURCE_DIRECTORIES:
        directory = root / dirname
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            if not path.name.startswith("_"):
                yield path


def load_records(root: Path) -> list[Record]:
    return [read_record(path, root) for path in iter_source_paths(root)]


def as_list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    return value if isinstance(value, list) else [value]


def linked_ids(record: Record) -> set[str]:
    result: set[str] = set()
    for field in LINK_FIELDS:
        for value in as_list(record.metadata.get(field)):
            text = str(value).strip()
            if text.startswith(ID_PREFIXES):
                result.add(text)
    return result


def estimate_tokens(text: str) -> int:
    """Return a conservative language-agnostic token estimate."""
    ascii_chars = sum(1 for char in text if ord(char) < 128)
    non_ascii_chars = len(text) - ascii_chars
    return max(1, (ascii_chars + 1) // 4 + (non_ascii_chars + 1) // 2)


def clip_text(text: str, max_chars: int, keep_tail: bool = False) -> str:
    text = text.strip()
    if len(text) <= max_chars:
        return text
    marker = "\n...[excerpt clipped]...\n"
    room = max(0, max_chars - len(marker))
    if keep_tail:
        return marker + text[-room:]
    head = room * 2 // 3
    tail = room - head
    return text[:head] + marker + text[-tail:]


def dump_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False)
