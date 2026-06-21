---
id: readme
type: documentation
title: "Novel Agent Scaffold"
status: seed
created: 2026-06-21
updated: 2026-06-21
tags:
  - documentation
  - scaffold
---
# Novel Agent Scaffold

This repository is a minimal scaffold for writing a novel with help from AI agents.

The source of truth is Markdown with YAML frontmatter. Story material, planning files, manuscript chapters, visual assets, and EPUB publishing output are kept in separate directories so agents can work on the right layer without confusing draft material with generated output.

## Structure

- `project.md`: working title, premise, constraints, and source map.
- `characters/`: character sheets and continuity facts.
- `world/`: setting, timeline, locations, rules, and world-state notes.
- `plot/`: whole-novel plot and plot-thread files.
- `materials/`: motifs, scene seeds, clues, research notes, dialogue seeds, and reusable ideas.
- `macguffins/`: MacGuffins, false leads, reveal timing, and payoff notes.
- `outlines/`: novel, act, sequence, and chapter outlines.
- `style/`: prose style guide and visual style guide.
- `assets/cover/`: cover image assets.
- `assets/illustrations/`: chapter illustrations, spot illustrations, motifs, and references.
- `chapters/`: manuscript source files such as `001.the-genesis.md`.
- `published/`: generated EPUB staging files and final EPUB output.
- `.agents/skills/`: repository-local Agent Skills for repeatable workflows.
- `scripts/`: deterministic project scripts.

## Local Skills

Use local skills for repeatable novel-building work:

- `$create-setting`: create or refine setting/worldbuilding files in `world/`.
- `$create-character`: create character files in `characters/`, including naming and gender fields.
- `$create-plot`: create whole-novel plots or plot threads in `plot/`.
- `$create-material`: create motifs, objects, clues, scene seeds, or research notes in `materials/`.
- `$create-visual-asset`: generate cover and illustration assets with a consistent visual style.
- `$build-epub`: render chapter Markdown, cover images, and illustrations into EPUB output.

Each creation skill starts from the user's prompt, proposes a structured first pass, asks for missing information or direction, loops on feedback, and writes a Markdown/frontmatter file only after confirmation.

## Typical Workflow

1. Set the working title, premise, and constraints in `project.md`.
2. Use `$create-setting` to establish the world and continuity rules.
3. Use `$create-character` to create the core cast.
4. Use `$create-material` for motifs, clues, objects, and scene seeds.
5. Use `$create-plot` to shape the central plot and supporting threads.
6. Draft chapter files in `chapters/` using sortable names such as `001.the-genesis.md`.
7. Use `$create-visual-asset` for the cover and any chapter illustrations.
8. Use `$build-epub` or `python3 scripts/build_epub.py` to generate the final EPUB.

## EPUB Output

The build script reads `chapters/*.md` in filename order, renders Markdown to XHTML, copies referenced local images into the EPUB package, includes a cover when available, and writes:

- intermediate EPUB files to `published/epub/`
- final EPUB to `published/novel.epub`

Generated EPUB output is ignored by Git by default. To change the book, edit source files first, then rebuild.

## Build Command

```bash
python3 scripts/build_epub.py
```

Useful options:

```bash
python3 scripts/build_epub.py --title "Working Title" --author "Author Name"
python3 scripts/build_epub.py --cover assets/cover/cover.png
python3 scripts/build_epub.py --output published/novel.epub
```

If no cover exists, use `$build-epub`; it will ask whether to create one with `$create-visual-asset` before building.
