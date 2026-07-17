---
id: readme
type: documentation
title: "Novel Agent Scaffold"
status: seed
created: 2026-06-21
updated: 2026-07-15
tags:
  - documentation
  - scaffold
---
# Novel Agent Scaffold

This repository is a minimal scaffold for writing a novel with help from AI agents.

The source of truth is Markdown with YAML frontmatter. Story material, planning files, manuscript chapters, visual assets, and EPUB publishing output are kept in separate directories so agents can work on the right layer without confusing draft material with generated output.

## Codex Plugin

The repository also contains an installable Codex plugin at
`plugins/novelist/`. Its repository marketplace manifest is
`.agents/plugins/marketplace.json`.

The plugin adds a `create-novel-project` initializer and packages the seven
repository-local writing skills. Plugin copies are generated from the canonical
`.agents/skills/` tree, while the initializer's source scaffold is stored under
`plugins/novelist/assets/scaffold/`.

Synchronize generated plugin content after changing a shared skill or scaffold
template:

```bash
python3 scripts/sync_novelist_plugin.py
python3 scripts/sync_novelist_plugin.py --check
```

See `plugins/novelist/README.md` for local marketplace installation and usage.

Public documentation, support, privacy terms, and release notes are available
at [novelist.comfuture.chatgpt.site](https://novelist.comfuture.chatgpt.site).

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
- `.agents/plugins/marketplace.json`: local Codex marketplace metadata.
- `plugins/novelist/`: installable Codex plugin distribution.
- `scripts/sync_novelist_plugin.py`: plugin skill and scaffold synchronization.

## Local Skills

Use local skills for repeatable novel-building work:

- `$create-setting`: create or refine setting/worldbuilding files in `world/`.
- `$create-character`: create character files in `characters/`, including naming and gender fields.
- `$create-plot`: create whole-novel plots or plot threads in `plot/`.
- `$create-material`: create motifs, objects, clues, scene seeds, or research notes in `materials/`.
- `$novel-story-telling`: control whole-novel flow, conflict escalation and resolution, chapter handoffs, reveals, and continuity across characters, timelines, world rules, clues, MacGuffins, and plot threads.
- `$create-visual-asset`: generate cover and illustration assets with a consistent visual style.
- `$publish-novel`: publish the manuscript, cover, and illustrations as a validated EPUB without requiring the author to run shell commands.

Each creation skill starts from the user's prompt, proposes a structured first pass, asks for missing information or direction, loops on feedback, and writes a Markdown/frontmatter file only after confirmation.

`$novel-story-telling` reads only the sources needed for the current task. Its bundled scripts build a token-bounded context pack, safely create a template-conformant chapter without overwriting an existing chapter number, run deterministic structural checks, and maintain a reviewed chapter-state ledger in `materials/000.story-ledger.md`. The skill then performs a semantic continuity gate for facts that cannot be checked mechanically. It includes focused references for general story flow, wuxia, science fiction, time travel and time loops, mystery, drama, and romantic entanglement.

The skill's internal prompts and scripts are written in English. Manuscript prose and author-facing creative output follow the language explicitly requested by the author, then the language configured in `project.md` or the style guide.

## Typical Workflow

1. Set the working title, premise, and constraints in `project.md`.
2. Use `$create-setting` to establish the world and continuity rules.
3. Use `$create-character` to create the core cast.
4. Use `$create-material` for motifs, clues, objects, and scene seeds.
5. Use `$create-plot` to shape the central plot and supporting threads.
6. Use `$novel-story-telling` to complete the story promise, escalation ladder, reveal plan, thread convergence, climax, resolution, and chapter-level handoffs.
7. Use `$novel-story-telling` before each chapter to assemble prior context, check continuity, and define the chapter contract.
8. Ask `$novel-story-telling` to write the approved draft through its chapter writer. It creates `chapters/NNN.lowercase-ascii-slug.md`, follows `chapters/_template.md`, refuses collisions, and immediately validates the result. After approval, update newly established canon and the story ledger.
9. Use `$create-visual-asset` for the cover and any chapter illustrations.
10. Ask `$publish-novel` to generate and validate the final EPUB.

## Example Prompts

The following sequence creates a character first, completes the novel's flow with that character in context, and then prepares and drafts a specific chapter.

### 1. Create A Character

```text
Use $create-character to create the protagonist for this novel.

She is a former royal archivist who can remember every written sentence but cannot recognize faces. She wants to prove that the kingdom's official history was altered, while hiding that she once helped destroy the original records. Give her a name appropriate to the existing setting, a public role, a private wound, a concrete desire, a deeper need, two conflicting relationships, one secret, and continuity facts that later chapters must preserve.

Read project.md, the current world files, plot files, and style guide before proposing the character. Present the first pass in Korean, ask me to confirm major canon decisions, and write the character file only after confirmation.
```

### 2. Complete The Novel's Story Flow

```text
Use $novel-story-telling to complete the whole-novel story flow from the current repository sources.

Read project.md and the relevant characters, materials, MacGuffins, plot threads, outlines, world rules, and style guide. Use the newly created former archivist as the protagonist. Define the reader promise, governing question, causal change chain, conflict escalation dimensions, active thread states, reveal and foreshadowing plan, midpoint reframe, crisis choice, climax mechanism, cost, aftermath, and chapter-to-chapter handoffs.

Choose mystery as the primary engine and drama as the secondary engine. Make every major reveal depend on evidence exposed earlier, and make the climax resolve through an established character decision and world rule rather than a newly introduced exception. Identify missing canon or contradictions instead of inventing answers silently. Present the proposed flow in Korean and update plot/ and outlines/ only after I approve it.
```

### 3. Prepare And Draft A Specific Chapter

```text
Use $novel-story-telling to prepare and draft Chapter 007, "The Burned Index."

First build a bounded context pack for Chapter 007 using the skill's scripts. Review the recent chapters, the target chapter outline, linked characters, active plot threads, world rules, relevant materials and MacGuffins, and the story continuity ledger. Run the structural continuity audit, then present a semantic continuity table and a chapter contract covering entry state, POV, time, location, immediate objective, opposition, clue exposure, relationship shift, irreversible change, exit state, and facts that must not change.

Do not begin prose until unresolved contradictions or required canon decisions are listed for approval. After approval, write the chapter in Korean while preserving the existing close-third voice and terminology. Use the skill's bundled chapter writer to create `chapters/007.the-burned-index.md` from a reviewed JSON payload; populate all template frontmatter, place prose in `## Draft`, preserve the required Synopsis and Revision Notes sections, refuse to overwrite any existing Chapter 007, and run the strict structural audit immediately after writing. When the chapter is accepted, update affected canonical source files and prepare a reviewed story-ledger fact card for Chapter 007.
```

## EPUB Output

The `$publish-novel` skill's bundled script reads `chapters/*.md` in filename
order and renders only each chapter's `## Draft` section to XHTML. The chapter
H1, Synopsis, and Revision Notes remain editorial source and are never included
in the book. The script copies local images referenced from Draft, includes a
cover when available, renders prose in sans serif and each exact `*“…”*` speech
range as `<i class="dialog">` in serif italics without changing Markdown
paragraph boundaries, and displays a standalone `---` as a centered `* * *`
scene ornament. It writes:

- an inspectable intermediate EPUB tree to `published/epub/`
- the ZIP-based reader artifact to `published/novel.epub`

Both generated forms are retained after publication and ignored by Git by
default. To change the book, edit source files first, then ask `$publish-novel`
to republish it.

## Publish Prompt

The author does not need to run a build command. Request publication with a prompt such as:

```text
Use $publish-novel to publish the current novel as an EPUB.

Read project.md and the publishable chapters, confirm the publication title, author or pen name, language, and cover, and warn me if any chapter is not final. If no cover exists, ask whether I want to create one with $create-visual-asset or continue without one. Then run the skill's bundled packaging script, validate the resulting EPUB, and report the final path, chapter count, packaged image count, and whether a cover was included.
```

By default, the skill retains intermediate files in `published/epub/` and the
final reader artifact in `published/novel.epub`. Generated output remains
ignored by Git unless explicitly added.
