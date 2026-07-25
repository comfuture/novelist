# Novelist Workspace

This workspace keeps the sources for one novel in structured Markdown so an
author and an agent can manage worldbuilding, characters, materials,
MacGuffins, plots, outlines, prose style, chapters, continuity, and reader
knowledge without losing their relationships.

EPUB publication is the final delivery step after the story sources and chapter
Drafts are approved.

## Use The Available Novelist Skills

The exact invocation syntax depends on the host:

- Codex plugin or local skills: `$create-character`
- Claude Code plugin: `/novelist:create-character`
- Claude Code standalone skills: `/create-character`
- Antigravity CLI: `/create-character`

The available writing skills are:

- `create-setting`
- `create-character`
- `create-material`
- `create-plot`
- `novel-story-telling`
- `create-visual-asset`
- `publish-novel`

Plugin-created workspaces use installed skills. Standalone exports contain
repository-local copies under `.agents/skills/`, `.claude/skills/`, or both.

## Source Structure

- `project.md`: premise, language, constraints, and source map.
- `characters/`: character sheets, relationships, motivations, and secrets.
- `world/`: settings, timelines, rules, locations, and institutions.
- `materials/`: motifs, research, objects, clues, dialogue seeds, and scenes.
- `macguffins/`: hidden functions, false leads, reveals, and payoffs.
- `plot/`: central plot and supporting plot threads.
- `outlines/`: novel, act, sequence, and chapter outlines.
- `style/`: prose and visual style guides.
- `chapters/`: canonical manuscript source in numeric filename order.
- `assets/cover/`: approved cover raster assets.
- `assets/illustrations/`: approved chapter and supporting raster assets.
- `published/`: generated staging and EPUB output; never canonical source.

Story source files use YAML frontmatter for stable indexing and references.
README and agent instruction files are documentation and do not require source
frontmatter.

## Writing Flow

1. Define the premise, language, and constraints in `project.md`.
2. Establish world rules and create the central cast.
3. Develop materials, MacGuffins, plots, and outlines.
4. Use the storytelling skill to choose genre strategies, control causality and
   escalation, plan reveals, converge threads, and define the climax.
5. Before a chapter, build a bounded context pack and review structural plus
   semantic continuity.
6. Approve the chapter contract before prose is written.
7. Create the guarded `chapters/NNN.lowercase-ascii-slug.md` file and validate
   its required `Synopsis`, `Draft`, and `Revision Notes` structure.
8. Update canonical facts and the reviewed story ledger after acceptance.
9. Create optional visual assets through a raster provider actually available
   to the current agent.
10. Publish only approved chapter Draft content as a validated EPUB.

## Visual Capability

The visual workflow always produces a style-locked prompt first. It may use a
host generator, a configured MCP or CLI tool, or an author-selected external
provider. If none is connected, the agent must preserve the prompt and state
that no image was generated.

## EPUB Delivery

The publication skill reads `chapters/*.md` in filename order and renders only
the unique `## Draft` section from each chapter. Synopsis and Revision Notes
remain editorial source.

Generated output includes:

- `published/epub/`: inspectable staging tree;
- `published/novel.epub`: validated reader artifact.

Change source files first, then regenerate. Coverless publication remains
supported after explicit author confirmation.
