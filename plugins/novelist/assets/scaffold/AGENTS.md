---
type: agent_instructions
project: novel-project
created: 2026-06-21
updated: 2026-07-31
---
# AGENTS.md

## Project Purpose

This repository is a source workspace for writing a novel. Treat Markdown files
under the story-source directories as source material or manuscript input for
the final book. Documentation files named `README.md`, `AGENTS.md`, and
`CLAUDE.md` are instructions rather than indexed story sources.

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
- Novelist plugin: installed Agent Skills for repeatable novel-writing workflows.

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

Chapter bodies are editorial containers with exactly one title H1 followed by
`## Synopsis`, `## Draft`, and `## Revision Notes` in that order. Only the
content inside `## Draft` is publishable manuscript. Synopsis and revision
notes remain source-only editorial material and must never appear in rendered
book output.

Inside `## Draft`, keep Markdown semantic and unambiguous:

- Separate paragraphs with one blank line.
- Write narration as plain paragraphs.
- Wrap each spoken range as exact `*“…”*`, whether it stands alone or shares a
  paragraph with narration, as in `*“Approved.”* Rhea said.` Curly double quotes
  identify speech; the surrounding Markdown emphasis becomes
  `<i class="dialog">` in EPUB.
- Let ordinary Markdown paragraph rules decide paragraph boundaries. A blank
  line creates a new paragraph; dialogue markup never creates one by itself.
- Reserve unquoted `*…*` for an interior thought. Use `‘…’` for quoted wording,
  remembered phrasing, or a quotation nested inside speech; do not use `“…”`
  for non-spoken mentions because the checker treats it as dialogue.
- Use `**…**` only for strong semantic emphasis. Balance markers on one line.
- Use inline backticks only for literal machine output, UI labels, filenames,
  code identifiers, or log text.
- Mark a scene or time break with `---` on its own line, with a blank line
  before and after it. Never use `* * *`, which can collide with list syntax.
- Do not use Markdown lists, blockquotes, or fenced code blocks anywhere inside
  Draft. H3 through H6 are reserved for genuine manuscript subheadings; never
  place another H2 inside Draft.

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

## Plugin Skills

Reusable novel-writing skills are supplied by the installed Novelist plugin.
Before handling repeatable novel-building work, use the matching plugin skill
for characters, settings, plots, materials, storytelling, visual assets, or
publication. Do not vendor a second `.agents/skills/` copy into the project
unless the author explicitly asks for repository-local skill ownership.

## Analytical Review Workflow

Use the analytical-review skill when the author explicitly asks to review an
outline, chapter, or manuscript. Review is read-only by default; do not change
planning files, chapters, canon, or generated output unless the author
separately authorizes selected revisions.

Only a fully autonomous request covering the complete lifecycle from initial
planning through publication automatically adds this bounded pre-publication
loop:

1. Inventory and review every publishable chapter.
2. Record each material finding as `apply`, `defer`, or `reject` with a concise
   rationale.
3. Apply selected revisions through the storytelling skill and update canonical
   state.
4. Run one focused regression review for prior high-impact findings and
   revision-introduced problems.
5. Run strict structural and continuity checks, then delegate EPUB packaging to
   the publication skill.

Do not infer this autonomous workflow from an ordinary planning, drafting,
revision, publish, export, build, regenerate, package, or validation request.
Ordinary publication retains its existing deterministic preflight and packaging
behavior without a literary-quality claim.

## Publishing Workflow

The intended publishing flow is:

1. Source material and manuscript live in Markdown files with frontmatter.
2. `chapters/*.md` are rendered in filename order.
3. Rendered intermediate files are written to `published/`.
4. The Novelist publication skill runs its bundled packaging script and validates the final `.epub` generated through staging under `published/`.

An ordinary publication request begins with the publication skill's existing
structural and continuity preflight. It does not automatically invoke
analytical review. The separate review loop above applies only when explicitly
requested or when the author delegates the fully autonomous
start-to-publication lifecycle.

Keep both generated forms: `published/epub/` is the inspectable staging tree,
and `published/*.epub` is the ZIP-based container opened by reading software.
Do not treat either as editable source. If the book needs changes, update source
files first, then regenerate.

Ask the available Novelist publication skill to generate and validate EPUB
output. The exact invocation syntax depends on the current agent host; the
skill runs its bundled script internally.
