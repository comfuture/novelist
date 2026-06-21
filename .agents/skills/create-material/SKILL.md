---
name: create-material
description: Create story material source files for the el_empiezo novel project. Use when the user wants to generate, refine, or save raw novel material such as motifs, objects, scene seeds, dialogue seeds, research notes, themes, images, conflicts, clues, or reusable ideas into materials/ as Markdown with YAML frontmatter.
---

# Create Material

## Overview

Use this skill to turn a rough story-material prompt into a complete `materials/*.md` source file.

Always follow `AGENTS.md` and `materials/_template.md`. Generate useful seed material from the prompt, ask for missing information and intended story use, revise from feedback, then write only after confirmation.

## Workflow

### 1. Read Context

Read:

- `AGENTS.md`
- `project.md`
- `materials/_template.md`
- Existing files in `materials/`
- Relevant `characters/`, `macguffins/`, `plot/`, `outlines/`, and `world/` files if referenced

### 2. Generate A Material Draft

From the user's prompt, infer a compact first-pass material note in Korean. Include:

- material category, such as `scene-seed`, `motif`, `object`, `line`, `research`, `theme`, `image`, `conflict`, or `clue`
- raw idea
- possible story use
- related characters, MacGuffins, plot threads, or settings
- whether it is canonical yet
- constraints, risks, or questions
- open decisions the user should make

Mark inferred items clearly. Keep uncertain ideas as `status: seed` and `canonical: false`.

### 3. Ask For Direction

Ask the user what role this material should play:

- background texture or major plot driver
- literal object or metaphor
- one-scene use or recurring motif
- clue, red herring, image system, dialogue seed, or research note
- canonical fact or scratch seed

Continue the feedback loop until the user says it is enough or gives enough detail to save.

### 4. Build The Material File

Use a filesystem-safe ASCII slug. Save to `materials/<slug>.md`; `id` must be `material-<slug>`.

Required frontmatter:

```yaml
id: material-ascii-slug
type: material
title: ""
category: scene-seed
status: seed
source: ""
canonical: false
related_characters: []
related_macguffins: []
plot_threads: []
used_in_chapters: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
```

The Markdown body must include:

- `# <title>`
- `## Idea`
- `## Story Use`
- `## Notes`

### 5. Write And Verify

Prefer the bundled script:

```bash
python3 .agents/skills/create-material/scripts/write_material.py --input /path/to/material.json --project-root .
```

Use a temporary JSON file with final confirmed data. The script writes `materials/<slug>.md`, refuses invalid slugs, and refuses to overwrite existing files unless `--force` is passed.

After writing, verify frontmatter delimiters, `type: material`, matching `id`, and `git status --short`. Do not commit unless the user asks.
