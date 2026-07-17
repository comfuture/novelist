---
name: create-setting
description: Create whole-novel setting and worldbuilding source files for this novel project. Use when the user wants to generate, refine, or save a novel setting, era, region, social order, locations, rules, atmosphere, constraints, or continuity facts into world/ as Markdown with YAML frontmatter.
---

# Create Setting

## Overview

Use this skill to turn a rough novel-setting prompt into a complete `world/*.md` source file.

Always follow `AGENTS.md` and `world/_template.md`. Generate useful defaults from the user's prompt, but keep the process interactive: reflect the inferred setting, ask for missing information and direction, revise from feedback, then write only after the user confirms.

Before running a bundled command, resolve `<skill-dir>` to the absolute directory
containing this `SKILL.md`. This keeps the same skill usable from either the
repository-local skill tree or the Novelist plugin.

## Workflow

### 1. Read Context

Read:

- `AGENTS.md`
- `project.md`
- `world/_template.md`
- Existing files in `world/`
- Relevant `plot/`, `outlines/`, `materials/`, `macguffins/`, and `characters/` files if the prompt references them

### 2. Generate A Setting Draft

From the user's prompt, infer a compact first-pass setting in Korean. Include:

- era and time scale
- primary region and key locations
- social order, institutions, class pressure, and power structure
- material culture and technology level
- atmosphere, sensory palette, and recurring visual motifs
- rules or constraints that affect plot
- continuity facts that should not drift
- open questions and missing decisions

Mark inferred items clearly. Do not present guesses as fixed canon.

### 3. Ask For Direction

Ask the user what to add, remove, sharpen, or decide. The question must focus on missing information and authorial direction, not on generic brainstorming.

Good prompts:

- "시대는 조선 후기 그대로 둘까요, 아니면 가상의 왕조로 비틀까요?"
- "이 세계의 핵심 압박을 정치, 가족, 종교, 경제 중 어디에 두면 좋을까요?"
- "현실 고증을 강하게 가져갈지, 분위기 우선으로 변형할지 선택해주세요."

Continue the feedback loop until the user says it is enough or gives enough detail to save.

### 4. Build The Setting File

Use a filesystem-safe ASCII slug. Save to `world/<slug>.md`; `id` must be `world-<slug>`.

Required frontmatter:

```yaml
id: world-ascii-slug
type: world
title: ""
category: setting
status: seed
time_period: ""
locations: []
rules: []
related_characters: []
related_materials: []
used_in_chapters: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
```

The Markdown body must include:

- `# <title>`
- `## Description`
- `## Story Pressure`
- `## Continuity`

### 5. Write And Verify

Prefer the bundled script:

```bash
python3 "<skill-dir>/scripts/write_setting.py" --input /path/to/setting.json --project-root .
```

Use a temporary JSON file with final confirmed data. The script writes `world/<slug>.md`, refuses invalid slugs, and refuses to overwrite existing files unless `--force` is passed.

After writing, verify frontmatter delimiters, `type: world`, matching `id`, and `git status --short`. Do not commit unless the user asks.
