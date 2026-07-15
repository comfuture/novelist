---
type: agent_instructions
project: novel-project
created: 2026-06-21
updated: 2026-07-15
---
# AGENTS.md

## Project Purpose

This repository is a source workspace for writing a novel. Treat every Markdown file outside this file as source material or manuscript input for the final book.

The canonical manuscript source is `chapters/`. Rendered output belongs in `published/` and is used later to produce the final `.epub`.

## Directory Roles

- `project.md`: project-level premise, genre, constraints, and source map.
- `characters/`: character sheets, relationship notes, motivations, secrets, and continuity facts.
- `materials/`: story material such as motifs, objects, research notes, dialogue seeds, scene seeds, themes, and references.
- `macguffins/`: MacGuffins, false leads, hidden functions, reveal timing, and resolution notes.
- `plot/`: plot threads, act structure, conflicts, reversals, reveals, and payoff tracking.
- `outlines/`: novel, act, sequence, and chapter outlines.
- `world/`: settings, locations, timelines, rules, institutions, and world-state continuity.
- `style/`: voice, point of view, tense, prose conventions, recurring terms, and revision preferences.
- `assets/`: project-bound cover and illustration image assets.
- `chapters/`: actual chapter manuscript files, sorted by filename.
- `published/`: generated render output only. Do not treat this as canonical source.
- `.agents/skills/`: repository-scoped Agent Skills for repeatable novel-writing workflows.

## Markdown And Frontmatter Rules

All source material files must be Markdown with YAML frontmatter.

Required frontmatter keys for source material:

- `id`: stable lowercase identifier, unique across the project.
- `type`: one of `project`, `documentation`, `character`, `material`, `macguffin`, `plot`, `outline`, `world`, `style_guide`, `chapter`, or `publishing_note`.
- `title` or `name`: human-readable label.
- `status`: one of `seed`, `outline`, `draft`, `revision`, `final`, or `archived`.
- `tags`: YAML array.
- `created`: ISO date, `YYYY-MM-DD`.
- `updated`: ISO date, `YYYY-MM-DD`.

Keep long prose, summaries, and draft text in the Markdown body. Use frontmatter for indexing, sorting, filtering, and references.

Use YAML arrays for links between files, for example:

```yaml
characters:
  - char-protagonist
materials:
  - material-red-thread
macguffins:
  - macguffin-locked-box
plot_threads:
  - plot-main
```

## Chapter Rules

Chapter source files live directly under `chapters/`.

Use filesystem-compatible filenames in this exact pattern:

```text
001.the-genesis.md
002.second-slug.md
003.final-slug.md
```

Rules:

- Use three zero-padded digits.
- Put one dot between the number and slug.
- Use lowercase ASCII slugs.
- Use hyphens instead of spaces.
- Avoid punctuation except the numeric dot and hyphens.
- Keep the frontmatter `number`, `id`, `title`, and filename in sync.
- Render chapters in numeric filename order.

Recommended chapter frontmatter:

```yaml
---
id: chapter-001
type: chapter
number: 1
title: "The Genesis"
slug: the-genesis
status: outline
pov: ""
timeline: ""
setting: ""
word_target: 2500
characters: []
materials: []
macguffins: []
plot_threads: []
outline: ""
published: false
created: 2026-06-21
updated: 2026-06-21
tags: []
---
```

## Writing Workflow

Before writing or revising a chapter:

1. Read the relevant files in `characters/`, `materials/`, `macguffins/`, `plot/`, `outlines/`, `world/`, and `style/`.
2. Check continuity facts before changing a character, timeline, setting, reveal, or MacGuffin.
3. Update source material files when a chapter introduces a new canonical fact.
4. Keep scratch ideas in `materials/` with `status: seed` until they become canonical.
5. Do not hand-edit generated files in `published/` unless explicitly asked.

When editing prose:

- Preserve the author's intended voice unless asked to rewrite style.
- Prefer minimal edits for continuity, grammar, or clarity.
- Do not destructively replace substantial draft text without explicit instruction.
- Summarize newly introduced facts after chapter changes.

## Subagent Use

If possible, use subagents for independent work such as continuity checks, outline review, style consistency review, or render verification. Reuse already open subagents in subsequent sessions when their context is relevant.

Keep delegated tasks concrete and non-overlapping. Do not let multiple agents edit the same source file at the same time.

## Local Skills

Project-specific reusable skills live in `.agents/skills/` so they are repository-scoped and portable to Codex-compatible Agent Skills tooling. Prefer this location over `.codex/skills` for checked-in project skills.

Before handling repeatable novel-building work, check `.agents/skills/` for a matching local skill and use it when applicable. Prefer these project skills for creating or refining characters, settings, plots, materials, MacGuffins, outlines, style guides, visual assets, publication, and chapter-related source files.

## Publishing Workflow

The intended publishing flow is:

1. Source material and manuscript live in Markdown files with frontmatter.
2. `chapters/*.md` are rendered in filename order.
3. Rendered intermediate files are written to `published/`.
4. The local `$publish-novel` skill runs its bundled packaging script and validates the final `.epub` generated through staging under `published/`.

Do not treat `.epub` output as editable source. If the book needs changes, update source files first, then regenerate.

Use the local `$publish-novel` skill to generate and validate EPUB output. The author should request publication with a prompt; the skill runs its bundled script internally.
