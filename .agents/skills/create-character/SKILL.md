---
name: create-character
description: Create character source files for the el_empiezo novel project. Use when the user wants to invent, refine, name, or save a fictional character into characters/ as Markdown with YAML frontmatter, especially from role, personality, setting, era, region, language, relationships, motives, secrets, or plot function.
---

# Create Character

## Overview

Use this skill to turn a rough character brief into a complete `characters/*.md` source file for this novel project.

Always follow the project's `AGENTS.md` and `characters/_template.md`. Keep the process interactive: refine the character first, then run a naming loop, then write the file only after the user confirms the final direction.

## Workflow

### 1. Gather And Reflect The Brief

Read existing context before asking questions:

- `AGENTS.md`
- `project.md`
- `characters/_template.md`
- Existing files in `characters/`
- Relevant `plot/`, `outlines/`, `world/`, `materials/`, or `macguffins/` files when the user references them

Restate the supplied role, character traits, and setting in Korean. Include:

- story role
- social role or occupation
- personality and behavioral texture
- era, region, class, language, nationality, and cultural background
- gender, including whether the character is gender-neutral
- relationship or plot function
- secrets, desires, conflicts, or contradictions if present

Ask what the user wants to add, remove, or sharpen. Continue this prompt loop until the user says it is enough or gives enough detail to proceed.

Do not create the character file during this stage.

### 2. Recommend Names

After the brief is sufficiently refined, propose about 10 names with short reasons.

Naming rules:

- If the character is Korean or lives as a Korean character in South Korea, recommend plausible Korean names in Hangul with family name and given name.
- If the setting gives a specific Korean era, region, class, or dialect background, reflect that context in the name choice and explain the reasoning.
- If the character is not Korean, keep both the original-language name and the Korean reading for use in the novel.
- If the original script is relevant, include it. Example: `Aleksandr Mikhailov / 알렉산드르 미하일로프`.
- If only a romanized original is appropriate, still include a Korean reading.
- Avoid copying the exact identity of a real living person unless the user explicitly requests a real person.
- Avoid joke names, overly symbolic names, and famous-name collisions unless the user asks for them.

For each option, show:

- displayed Korean name or Korean reading
- original name when non-Korean
- name language or cultural context
- reason it fits the role, personality, and setting

Ask the user to choose a name, request revisions, or provide a new naming direction. Continue this prompt loop until one final name is selected.

### 3. Build The Character Sheet

Create a complete character sheet using the selected name and refined brief.

Required frontmatter keys:

```yaml
id: char-ascii-slug
type: character
name: "김하나"
original_name: "김하나"
korean_reading: "김하나"
name_language: ko
name_context: "현대 대한민국"
aliases: []
role: ""
status: seed
age: ""
gender: ""
pronouns: ""
first_appearance: ""
last_seen: ""
relationships: []
wants: []
needs: []
conflicts: []
secrets: []
related_materials: []
related_macguffins: []
plot_threads: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
```

Use an ASCII filesystem slug, such as `kim-hana`, `alexandr-mikhailov`, or `old-palace-guard`. The file path must be `characters/<slug>.md`, and `id` must be `char-<slug>`.

Set `gender` explicitly when the user provides or confirms it. If the character is gender-neutral, use `gender: "성별 중립"` and keep pronouns or honorific usage consistent with the setting. If gender is intentionally undecided, ask once before writing; only use `gender: "미정"` when the user wants it left undecided.

The Markdown body must include these sections:

- `# <name>`
- `## Function`
- `## Surface`
- `## Interior`
- `## Relationships`
- `## Continuity`

Keep unknown values as empty strings or empty arrays instead of inventing hard canon.

### 4. Write The File

Prefer the bundled script:

```bash
python3 .agents/skills/create-character/scripts/write_character.py --input /path/to/character.json --project-root .
```

Use a temporary JSON file containing the final agreed character data. The script writes `characters/<slug>.md`, refuses invalid slugs, and refuses to overwrite existing files unless `--force` is passed.

If the script is unavailable, create the Markdown file manually with the same frontmatter and body shape.

### 5. Verify

After writing:

- Confirm the file starts and ends frontmatter with `---`.
- Confirm `type: character`.
- Confirm `id` matches the filename slug.
- Confirm non-Korean characters include both `original_name` and `korean_reading`.
- Run `git status --short` and report the changed files.

Do not commit unless the user asks.
