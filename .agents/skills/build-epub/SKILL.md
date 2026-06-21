---
name: build-epub
description: Build this novel project into an EPUB from chapters Markdown, cover images, and illustrations. Use when the user wants to render, package, validate, or regenerate published EPUB output from chapters/ and project assets, including checking for a missing cover and coordinating cover generation before the build.
---

# Build EPUB

## Overview

Use this skill to render `chapters/*.md` into a complete `.epub` under `published/`.

The canonical source remains Markdown and project assets. Generated files in `published/` are output, not source.

## Required Context

Read before building:

- `AGENTS.md`
- `project.md`
- `published/README.md`
- `chapters/*.md`
- `style/visual-style-guide.md`
- existing `assets/cover/` and `assets/illustrations/`

## Cover Check

Before running the build, check for a usable cover in this order:

1. a user-provided `--cover` path
2. `cover_image` in `project.md` frontmatter
3. `assets/cover/cover.png`, `.jpg`, `.jpeg`, or `.webp`

If no cover exists, ask whether to generate one. Ask for the desired feeling, central image, and whether the cover should include text. If the user wants a cover, use `$create-visual-asset` first and save the result under `assets/cover/`, then continue the EPUB build.

Do not block EPUB generation merely because there is no cover if the user explicitly wants to build without one.

## Build Command

Run:

```bash
python3 scripts/build_epub.py
```

Useful options:

```bash
python3 scripts/build_epub.py --title "Working Title" --author "Author Name"
python3 scripts/build_epub.py --cover assets/cover/cover.png
python3 scripts/build_epub.py --output published/novel.epub
```

The script:

- reads chapter files from `chapters/` in filename order
- ignores template files such as `_template.md`
- converts chapter Markdown to XHTML
- copies referenced local images into the EPUB
- includes a cover image when available
- writes rendered intermediate files to `published/epub/`
- writes the final EPUB file to `published/novel.epub` by default

## Chapter Image Rules

Chapter images must use normal Markdown image syntax:

```markdown
![Alt text](../assets/illustrations/001-scene.png)
```

Use relative project-local image paths. External HTTP images are not packaged.

## Verification

After building:

- Confirm the `.epub` file exists and is non-empty.
- Confirm `published/epub/OEBPS/content.opf` exists.
- Confirm all referenced chapter images were copied into `published/epub/OEBPS/images/`.
- Run `python3 scripts/build_epub.py` in a temporary project if changing the script itself.
- Run `git status --short` and report generated output separately from source changes.

Do not commit generated `published/*.epub` or `published/epub/` unless the user explicitly asks.
