---
name: create-plot
description: Create whole-novel plot and plot-thread source files for this novel project. Use when the user wants to generate, refine, structure, or save a central plot, act structure, promise, pressure, reversals, turns, reveals, or payoffs into plot/ as Markdown with YAML frontmatter.
---

# Create Plot

## Overview

Use this skill to turn a rough plot prompt into a complete `plot/*.md` source file.

Always follow `AGENTS.md` and `plot/_template.md`. Generate a workable plot skeleton from the user's prompt, ask for missing information and desired direction, revise through feedback, then write only after confirmation.

## Workflow

### 1. Read Context

Read:

- `AGENTS.md`
- `project.md`
- `plot/_template.md`
- `plot/000.master-plot.md`
- Existing files in `plot/`
- Relevant `outlines/`, `world/`, `characters/`, `materials/`, and `macguffins/` files if referenced

### 2. Generate A Plot Draft

From the user's prompt, infer a compact first-pass plot in Korean. Include:

- story promise
- protagonist pressure and opposition
- inciting incident
- core conflict
- act or sequence shape
- midpoint reversal
- lowest point
- climax choice
- resolution shape
- setups, reveals, and payoffs
- open questions and missing decisions

Mark inferred items clearly. Do not lock major canon facts without user confirmation.

### 3. Ask For Direction

Ask the user what to strengthen, remove, or decide. Focus on plot decisions with real consequences:

- emotional ending vs ironic ending
- external conflict vs internal conflict
- mystery-first, thriller-first, romance-first, or literary-first structure
- single protagonist vs ensemble pressure
- reveal timing and whether the reader knows more than the characters

Continue the feedback loop until the user says it is enough or gives enough detail to save.

### 4. Build The Plot File

Use a filesystem-safe ASCII slug. Save to `plot/<slug>.md`; `id` must be `plot-<slug>`.

Required frontmatter:

```yaml
id: plot-ascii-slug
type: plot
title: ""
scope: novel
status: seed
starts_in: ""
turns_in: []
pays_off_in: ""
characters: []
materials: []
macguffins: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
```

Use `scope: novel` for the whole-book plot and `scope: thread` for a subplot or plot thread.

The Markdown body must include:

- `# <title>`
- `## Promise`
- `## Pressure`
- `## Turns`

### 5. Write And Verify

Prefer the bundled script:

```bash
python3 .agents/skills/create-plot/scripts/write_plot.py --input /path/to/plot.json --project-root .
```

Use a temporary JSON file with final confirmed data. The script writes `plot/<slug>.md`, refuses invalid slugs, and refuses to overwrite existing files unless `--force` is passed.

After writing, verify frontmatter delimiters, `type: plot`, matching `id`, and `git status --short`. Do not commit unless the user asks.
