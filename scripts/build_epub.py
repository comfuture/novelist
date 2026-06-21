#!/usr/bin/env python3
"""Build an EPUB from the novel markdown scaffold."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import mimetypes
import re
import shutil
import sys
import uuid
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CHAPTER_RE = re.compile(r"^[0-9]{3}\.[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
COVER_CANDIDATES = ("cover.png", "cover.jpg", "cover.jpeg", "cover.webp")


@dataclass
class Chapter:
    source: Path
    title: str
    body: str
    output_name: str


@dataclass
class ImageAsset:
    source: Path
    epub_name: str
    media_type: str
    is_cover: bool = False


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value == "":
        return ""
    if value == "[]":
        return []
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return [item.strip().strip('"') for item in value[1:-1].split(",") if item.strip()]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw_frontmatter = text[4:end].splitlines()
    body_start = end + len("\n---")
    if body_start < len(text) and text[body_start] == "\n":
        body_start += 1

    data: dict[str, Any] = {}
    current_key: str | None = None
    for line in raw_frontmatter:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") and current_key:
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            data[current_key].append(parse_scalar(stripped[2:]))
            continue
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value == "":
            data[key] = []
            current_key = key
        else:
            data[key] = parse_scalar(value)
            current_key = key if isinstance(data[key], list) else None
    return data, text[body_start:]


def load_markdown(path: Path) -> tuple[dict[str, Any], str]:
    return parse_frontmatter(path.read_text(encoding="utf-8"))


def first_heading(body: str) -> str | None:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def title_from_filename(path: Path) -> str:
    stem = path.stem
    if "." in stem:
        stem = stem.split(".", 1)[1]
    return stem.replace("-", " ").title()


def discover_chapters(chapters_dir: Path) -> list[Chapter]:
    files = [
        path
        for path in chapters_dir.glob("*.md")
        if not path.name.startswith("_") and CHAPTER_RE.match(path.name)
    ]
    chapters: list[Chapter] = []
    for index, path in enumerate(sorted(files), 1):
        frontmatter, body = load_markdown(path)
        title = str(frontmatter.get("title") or first_heading(body) or title_from_filename(path))
        output_name = f"chapter-{index:03d}.xhtml"
        chapters.append(Chapter(path, title, body, output_name))
    return chapters


def project_metadata(project_root: Path) -> dict[str, Any]:
    path = project_root / "project.md"
    if not path.exists():
        return {}
    frontmatter, _ = load_markdown(path)
    return frontmatter


def find_cover(project_root: Path, metadata: dict[str, Any], explicit_cover: str | None) -> Path | None:
    if explicit_cover:
        candidate = Path(explicit_cover)
        if not candidate.is_absolute():
            candidate = project_root / candidate
        return candidate.resolve()

    cover_value = metadata.get("cover_image")
    if cover_value:
        candidate = Path(str(cover_value))
        if not candidate.is_absolute():
            candidate = project_root / candidate
        return candidate.resolve()

    cover_dir = project_root / "assets" / "cover"
    for filename in COVER_CANDIDATES:
        candidate = cover_dir / filename
        if candidate.exists():
            return candidate.resolve()
    return None


def media_type(path: Path) -> str:
    guessed, _ = mimetypes.guess_type(path.name)
    if guessed:
        return guessed
    suffix = path.suffix.lower()
    if suffix == ".webp":
        return "image/webp"
    if suffix == ".xhtml":
        return "application/xhtml+xml"
    return "application/octet-stream"


def unique_image_name(source: Path, used: set[str]) -> str:
    base = source.name.lower().replace(" ", "-")
    candidate = base
    index = 2
    while candidate in used:
        candidate = f"{source.stem}-{index}{source.suffix}".lower().replace(" ", "-")
        index += 1
    used.add(candidate)
    return candidate


def resolve_local_image(
    project_root: Path,
    base_dir: Path,
    raw_target: str,
    image_assets: dict[Path, ImageAsset],
    used_names: set[str],
) -> str:
    target = raw_target.strip().split()[0]
    if target.startswith("http://") or target.startswith("https://"):
        raise SystemExit(f"External images cannot be packaged in EPUB: {target}")
    candidate = Path(target)
    if not candidate.is_absolute():
        candidate = (base_dir / candidate).resolve()
        if not candidate.exists():
            fallback = (project_root / target).resolve()
            if fallback.exists():
                candidate = fallback
    if not candidate.exists():
        raise SystemExit(f"Image not found: {raw_target}")

    source = candidate.resolve()
    if source not in image_assets:
        epub_name = unique_image_name(source, used_names)
        image_assets[source] = ImageAsset(source, epub_name, media_type(source))
    return f"../images/{image_assets[source].epub_name}"


def render_inlines(text: str, resolve_image: Any | None = None) -> str:
    image_tokens: dict[str, str] = {}

    def replace_image(match: re.Match[str]) -> str:
        if resolve_image is None:
            return match.group(0)
        alt, target = match.groups()
        token = f"\ue000image-{len(image_tokens)}\ue000"
        src = resolve_image(target)
        image_tokens[token] = (
            f'<img class="inline-image" src="{html.escape(src, quote=True)}" '
            f'alt="{html.escape(alt, quote=True)}" />'
        )
        return token

    text = IMAGE_RE.sub(replace_image, text)
    escaped = html.escape(text, quote=True)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    escaped = LINK_RE.sub(
        lambda match: f'<a href="{html.escape(match.group(2), quote=True)}">{match.group(1)}</a>',
        escaped,
    )
    for token, replacement in image_tokens.items():
        escaped = escaped.replace(token, replacement)
    return escaped


def render_markdown(
    body: str,
    chapter_path: Path,
    project_root: Path,
    image_assets: dict[Path, ImageAsset],
    used_names: set[str],
) -> str:
    html_lines: list[str] = []
    paragraph: list[str] = []
    list_mode: str | None = None
    code_mode = False
    code_lines: list[str] = []

    def close_list() -> None:
        nonlocal list_mode
        if list_mode:
            html_lines.append(f"</{list_mode}>")
            list_mode = None

    def inline(text: str) -> str:
        return render_inlines(
            text,
            lambda target: resolve_local_image(
                project_root,
                chapter_path.parent,
                target,
                image_assets,
                used_names,
            ),
        )

    def flush_paragraph() -> None:
        if paragraph:
            html_lines.append(f"<p>{inline(' '.join(paragraph))}</p>")
            paragraph.clear()

    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            if code_mode:
                html_lines.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines.clear()
                code_mode = False
            else:
                flush_paragraph()
                close_list()
                code_mode = True
            continue
        if code_mode:
            code_lines.append(line)
            continue

        if not stripped:
            flush_paragraph()
            close_list()
            continue

        image_match = IMAGE_RE.fullmatch(stripped)
        if image_match:
            flush_paragraph()
            close_list()
            alt, target = image_match.groups()
            src = resolve_local_image(project_root, chapter_path.parent, target, image_assets, used_names)
            html_lines.append(
                f'<figure><img src="{html.escape(src, quote=True)}" alt="{html.escape(alt, quote=True)}" /></figure>'
            )
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            html_lines.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            continue

        unordered = re.match(r"^[-*]\s+(.+)$", stripped)
        if unordered:
            flush_paragraph()
            if list_mode != "ul":
                close_list()
                html_lines.append("<ul>")
                list_mode = "ul"
            html_lines.append(f"<li>{inline(unordered.group(1))}</li>")
            continue

        ordered = re.match(r"^[0-9]+\.\s+(.+)$", stripped)
        if ordered:
            flush_paragraph()
            if list_mode != "ol":
                close_list()
                html_lines.append("<ol>")
                list_mode = "ol"
            html_lines.append(f"<li>{inline(ordered.group(1))}</li>")
            continue

        quote = re.match(r"^>\s+(.+)$", stripped)
        if quote:
            flush_paragraph()
            close_list()
            html_lines.append(f"<blockquote><p>{inline(quote.group(1))}</p></blockquote>")
            continue

        paragraph.append(stripped)

    if code_mode:
        html_lines.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    flush_paragraph()
    close_list()
    return "\n".join(html_lines)


def xhtml_page(title: str, body_html: str, language: str) -> str:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{html.escape(language, quote=True)}" lang="{html.escape(language, quote=True)}">
<head>
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="../styles.css" />
</head>
<body>
  <section epub:type="chapter">
{body_html}
  </section>
</body>
</html>
'''


def cover_page(title: str, cover_asset: ImageAsset, language: str) -> str:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{html.escape(language, quote=True)}" lang="{html.escape(language, quote=True)}">
<head>
  <title>{html.escape(title)} Cover</title>
  <link rel="stylesheet" type="text/css" href="styles.css" />
</head>
<body>
  <section epub:type="cover" class="cover">
    <img src="images/{html.escape(cover_asset.epub_name, quote=True)}" alt="{html.escape(title, quote=True)} cover" />
  </section>
</body>
</html>
'''


def nav_page(title: str, chapters: list[Chapter], has_cover: bool, language: str) -> str:
    items = []
    if has_cover:
        items.append('<li><a href="cover.xhtml">Cover</a></li>')
    for chapter in chapters:
        items.append(
            f'<li><a href="chapters/{chapter.output_name}">{html.escape(chapter.title)}</a></li>'
        )
    toc = "\n      ".join(items)
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{html.escape(language, quote=True)}" lang="{html.escape(language, quote=True)}">
<head>
  <title>{html.escape(title)} Navigation</title>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>{html.escape(title)}</h1>
    <ol>
      {toc}
    </ol>
  </nav>
</body>
</html>
'''


def content_opf(
    book_id: str,
    title: str,
    author: str,
    language: str,
    chapters: list[Chapter],
    images: list[ImageAsset],
    has_cover: bool,
) -> str:
    modified = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />',
        '<item id="style" href="styles.css" media-type="text/css" />',
    ]
    if has_cover:
        manifest.append('<item id="cover-page" href="cover.xhtml" media-type="application/xhtml+xml" />')
    for index, chapter in enumerate(chapters, 1):
        manifest.append(
            f'<item id="chapter-{index:03d}" href="chapters/{chapter.output_name}" media-type="application/xhtml+xml" />'
        )
    for index, image in enumerate(images, 1):
        properties = ' properties="cover-image"' if image.is_cover else ""
        manifest.append(
            f'<item id="image-{index:03d}" href="images/{html.escape(image.epub_name, quote=True)}" media-type="{html.escape(image.media_type, quote=True)}"{properties} />'
        )

    spine = []
    if has_cover:
        spine.append('<itemref idref="cover-page" linear="no" />')
    for index, _chapter in enumerate(chapters, 1):
        spine.append(f'<itemref idref="chapter-{index:03d}" />')

    return f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">{html.escape(book_id)}</dc:identifier>
    <dc:title>{html.escape(title)}</dc:title>
    <dc:creator>{html.escape(author)}</dc:creator>
    <dc:language>{html.escape(language)}</dc:language>
    <meta property="dcterms:modified">{modified}</meta>
  </metadata>
  <manifest>
    {chr(10).join("    " + item for item in manifest)}
  </manifest>
  <spine>
    {chr(10).join("    " + item for item in spine)}
  </spine>
</package>
'''


def stylesheet() -> str:
    return """body {
  font-family: serif;
  line-height: 1.65;
  margin: 5%;
}
h1, h2, h3 {
  line-height: 1.25;
}
figure {
  margin: 1.5em 0;
  text-align: center;
}
img {
  max-width: 100%;
  height: auto;
}
.inline-image {
  max-height: 1.2em;
  vertical-align: middle;
}
.cover {
  margin: 0;
  padding: 0;
  text-align: center;
}
.cover img {
  max-height: 100vh;
}
"""


def container_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def safe_staging_dir(project_root: Path, staging_dir: Path) -> Path:
    resolved = staging_dir.resolve()
    published_root = (project_root / "published").resolve()
    try:
        resolved.relative_to(published_root)
    except ValueError as exc:
        raise SystemExit("--staging-dir must be a generated subdirectory under published/") from exc
    if resolved == published_root:
        raise SystemExit("--staging-dir must not be the published/ directory itself")
    return resolved


def build(args: argparse.Namespace) -> Path:
    project_root = args.project_root.resolve()
    metadata = project_metadata(project_root)
    title = args.title or str(metadata.get("title") or "Untitled Novel")
    author = args.author or str(metadata.get("author") or "Unknown Author")
    language = args.language or str(metadata.get("language") or "ko")

    chapters = discover_chapters(project_root / args.chapters_dir)
    if not chapters:
        raise SystemExit(f"No chapter files found in {args.chapters_dir}/")

    output_path = project_root / args.output
    staging_dir = safe_staging_dir(project_root, project_root / args.staging_dir)
    cover_path = find_cover(project_root, metadata, args.cover)

    if cover_path and not cover_path.exists():
        raise SystemExit(f"Cover image not found: {cover_path}")

    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    (staging_dir / "META-INF").mkdir(parents=True)
    (staging_dir / "OEBPS" / "chapters").mkdir(parents=True)
    (staging_dir / "OEBPS" / "images").mkdir(parents=True)

    image_assets: dict[Path, ImageAsset] = {}
    used_image_names: set[str] = set()
    cover_asset: ImageAsset | None = None
    if cover_path:
        cover_source = cover_path.resolve()
        cover_asset = ImageAsset(
            cover_source,
            unique_image_name(cover_source, used_image_names),
            media_type(cover_source),
            is_cover=True,
        )
        image_assets[cover_source] = cover_asset

    write_text(staging_dir / "mimetype", "application/epub+zip")
    write_text(staging_dir / "META-INF" / "container.xml", container_xml())
    write_text(staging_dir / "OEBPS" / "styles.css", stylesheet())

    for chapter in chapters:
        body_html = render_markdown(
            chapter.body,
            chapter.source,
            project_root,
            image_assets,
            used_image_names,
        )
        write_text(
            staging_dir / "OEBPS" / "chapters" / chapter.output_name,
            xhtml_page(chapter.title, body_html, language),
        )

    image_list = list(image_assets.values())
    for image in image_list:
        shutil.copy2(image.source, staging_dir / "OEBPS" / "images" / image.epub_name)

    if cover_asset:
        write_text(staging_dir / "OEBPS" / "cover.xhtml", cover_page(title, cover_asset, language))

    write_text(staging_dir / "OEBPS" / "nav.xhtml", nav_page(title, chapters, bool(cover_asset), language))
    write_text(
        staging_dir / "OEBPS" / "content.opf",
        content_opf(
            f"urn:uuid:{uuid.uuid4()}",
            title,
            author,
            language,
            chapters,
            image_list,
            bool(cover_asset),
        ),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()

    with zipfile.ZipFile(output_path, "w") as epub:
        epub.write(staging_dir / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(staging_dir.rglob("*")):
            if path.is_dir() or path.name == "mimetype":
                continue
            epub.write(path, path.relative_to(staging_dir), compress_type=zipfile.ZIP_DEFLATED)

    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path("."))
    parser.add_argument("--chapters-dir", default="chapters")
    parser.add_argument("--staging-dir", default="published/epub")
    parser.add_argument("--output", default="published/novel.epub")
    parser.add_argument("--cover", default=None)
    parser.add_argument("--title", default=None)
    parser.add_argument("--author", default=None)
    parser.add_argument("--language", default=None)
    args = parser.parse_args()

    output = build(args)
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
