---
name: publish-novel
description: Publish this Markdown novel project as a validated EPUB using the skill's bundled packaging script. Use when the author asks to publish, export, build, regenerate, package, or validate the novel or EPUB; when checking publication metadata, chapter readiness, covers, illustrations, generated output, or EPUB integrity; or when coordinating a missing cover before publication.
---

# Publish Novel

## Operating Contract

Turn an author request such as "Publish this novel" into the complete EPUB workflow. Do not ask the author to type shell commands. Run the bundled script yourself, verify the result, and report the artifact path.

Treat Markdown and project assets as canonical source. Treat `published/epub/` and `.epub` files as generated output. Never repair a generated EPUB by hand; update source and republish.

Interpret `publish` as local EPUB generation only. Do not upload, distribute, email, release, or submit the book to a storefront or external service unless the author explicitly requests that separate action.

## Workflow

### 1. Read Publication Context

Read:

- `AGENTS.md`
- `project.md`
- `published/README.md`
- publishable chapter filenames and frontmatter, plus image references needed for packaging
- `style/visual-style-guide.md`
- existing files under `assets/cover/` and `assets/illustrations/`

Preserve the manuscript language and project terminology.

Do not load the full prose of every chapter into model context. Let the bundled script stream chapter bodies during rendering. Read chapter prose only when diagnosing a rendering, image, or metadata problem.

### 2. Run Preflight

Confirm:

- at least one chapter matches `NNN.ascii-slug.md`;
- chapter numbers and filenames are in the intended order;
- the requested manuscript is complete enough to publish;
- title, author or pen name, and language are known;
- all local Markdown image references exist;
- the output and staging paths remain under the intended project.

If any chapter is not `final`, list it and ask for confirmation before publishing unless the author explicitly requests a draft or proof EPUB.

If the title is empty or still a placeholder, ask for the publication title. If the author is missing, ask for the author or pen name; do not silently publish as `Unknown Author` without confirmation. Pass one-time metadata as script options. Update `project.md` only when the author asks to make it canonical.

### 3. Resolve The Cover

Find a cover in this order:

1. a path explicitly supplied by the author;
2. `cover_image` in `project.md` frontmatter;
3. `assets/cover/cover.png`, `.jpg`, `.jpeg`, or `.webp`.

If no cover exists, ask whether to create one or publish without one. When the author wants a cover, use `$create-visual-asset`, save it under `assets/cover/`, verify the final image, and resume publication. Do not block a coverless publication after the author confirms that choice.

### 4. Publish

Run the bundled script from the repository root:

```bash
python3 .agents/skills/publish-novel/scripts/build_epub.py \
  --project-root .
```

Add only the options needed for confirmed metadata or output choices:

```bash
python3 .agents/skills/publish-novel/scripts/build_epub.py \
  --project-root . \
  --title "Publication Title" \
  --author "Author or Pen Name" \
  --language ko \
  --cover assets/cover/cover.png \
  --output published/novel.epub
```

The script must:

- render numbered chapter Markdown in filename order;
- ignore template files;
- package block and inline local images;
- include the selected cover when present;
- keep staging inside `published/epub/` by default;
- write `published/novel.epub` by default;
- validate the final archive automatically.

### 5. Verify And Report

Require the script's successful validation report. It checks:

- a non-empty ZIP-compatible EPUB;
- the first, uncompressed `mimetype` entry;
- required container, navigation, package, and stylesheet members;
- at least one rendered chapter;
- well-formed XML and XHTML;
- packaged targets for local `href` and `src` references.

To validate an existing artifact without rebuilding, run:

```bash
python3 .agents/skills/publish-novel/scripts/build_epub.py \
  --project-root . \
  --validate-only published/novel.epub
```

Report:

- the absolute EPUB path;
- title, author, and language used;
- chapter and packaged-image counts;
- whether a cover was included;
- any warnings or intentionally accepted draft conditions.

Run `git status --short` and separate generated ignored output from source changes. Do not commit `published/*.epub` or `published/epub/` unless the author explicitly asks.

## Failure Handling

- Stop when no publishable chapter exists.
- Stop when a referenced local image is missing.
- Stop when the cover path is invalid.
- Stop when staging points outside a generated subdirectory of `published/`.
- Stop when the EPUB output points outside `published/` or inside its staging directory.
- Stop when EPUB validation fails; report the exact member or reference and repair the canonical source or bundled script before rebuilding.
- Never claim publication success from file existence alone.
