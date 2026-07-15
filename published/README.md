---
id: published-readme
type: publishing_note
title: "Published Output"
status: seed
source: chapters
generated: true
formats:
  - markdown
  - html
  - epub
created: 2026-06-21
updated: 2026-07-15
tags: []
---
# Published Output

This directory is for rendered artifacts generated from `chapters/`.

Do not edit generated book output directly. Update source material or chapter files, then regenerate the published files and final `.epub`.

Use the repository-local `$publish-novel` skill to generate and validate these artifacts from an author publication request.

Chapter source files are editorial containers. Publication renders only the
content inside each chapter's unique `## Draft` section, with the chapter title
supplied from canonical metadata. `## Synopsis` and `## Revision Notes` are
writer-facing material and must not appear in EPUB chapter XHTML. A standalone
`---` in Draft is the canonical scene break and renders as a semantic separator
with a centered `* * *` ornament, not a list. Prose paragraphs render with a
sans-serif stack. Each exact `*“…”*` speech range becomes
`<i class="dialog">` in a serif italic stack without creating a paragraph,
while unquoted `*…*` remains interior thought rendered as `<em>`.

Publication retains both generated forms:

- `published/epub/` is the inspectable staging tree;
- `published/*.epub` is the ZIP-based container used by reading software, with
  `mimetype` first and uncompressed as required by EPUB packaging.

Rebuilding may replace the staging contents, but successful packaging does not
delete the staging directory.
