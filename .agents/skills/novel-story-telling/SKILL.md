---
name: novel-story-telling
description: Design and control whole-novel storytelling, chapter-to-chapter flow, conflict escalation and resolution, reveals, foreshadowing, continuity, safe chapter-file creation, and next-chapter handoffs for this Markdown novel repository. Use when planning, drafting, or revising story structure, preparing or writing the next chapter from prior context, creating a template-conformant chapter under chapters/, checking contradictions, maintaining story-state summaries, selecting genre-specific narrative devices, or auditing character, timeline, world-rule, clue, MacGuffin, and plot-thread continuity.
---

# Novel Story Telling

## Operating Contract

Treat `chapters/` as manuscript canon and all other source directories as planning and continuity evidence. Follow `AGENTS.md`. Never edit `published/` as source.

Write all agent instructions, temporary prompts, schemas, and script inputs in English. Write manuscript prose and author-facing creative output in this order of precedence:

1. the language explicitly requested by the author;
2. `project.md` `language`;
3. `style/000.style-guide.md` `language`;
4. the dominant language of recent chapters.

Preserve names, honorifics, invented terms, and spelling from canonical files. Do not translate them unless requested.

Resolve conflicts by authority: explicit author direction > `final` source > `revision` source > latest manuscript fact > `draft` source > outline or seed. Report unresolved conflicts; do not silently choose or invent canon.

## Core Workflow

### 1. Orient

Read `AGENTS.md`, `project.md`, `style/000.style-guide.md`, `plot/000.master-plot.md`, and `outlines/000.master-outline.md`. Determine:

- output language and prose constraints;
- current story promise and governing question;
- target chapter and its irreversible change;
- active plot threads, promises, clues, and MacGuffins;
- current character knowledge, desire, condition, relationship, and location;
- hard world rules and timeline constraints.

Do not load every source file into context by default.

### 2. Build A Bounded Context Pack

Run:

```bash
python3 .agents/skills/novel-story-telling/scripts/build_story_context.py \
  --project-root . \
  --chapter <number> \
  --query "<POV, location, entities, conflict, or theme>" \
  --max-tokens 6000 \
  --output-language auto \
  --output /tmp/story-context.md
```

Read the resulting pack. It prioritizes explicit links, active master sources, the target outline, recent chapters, the story ledger, and query matches. It includes source paths so every inferred constraint can be checked against canon.

Increase the budget only when the pack proves insufficient. Prefer linked fact cards and `Continuity` sections over full old chapters. Read a full source file only to resolve ambiguity or recover scene-level nuance.

### 3. Select Narrative Structure

Read [story-flow.md](references/story-flow.md) for whole-book and chapter-unit control. Read only the genre references needed for the current project:

- [wuxia.md](references/wuxia.md) for jianghu ethics, obligations, factions, techniques, and reputation;
- [science-fiction.md](references/science-fiction.md) for speculative premises, system consequences, and rule-bound solutions;
- [time-travel-and-loop.md](references/time-travel-and-loop.md) for temporal ontologies, causal state, and repeated-loop progression;
- [mystery.md](references/mystery.md) for fair clues, truth timelines, suspect logic, and reveal control;
- [drama.md](references/drama.md) for relationship pressure, recognition, reversal, and costly repair;
- [romantic-entanglement.md](references/romantic-entanglement.md) for jealousy, triangle dynamics, intimacy allocation, betrayal, and relational aftermath.

For hybrids, select one primary story engine and at most two secondary engines per chapter. Preserve each genre's reader contract. For example, a romantic subplot may intensify a mystery, but it must not excuse an unseeded solution.

### 4. Establish The Story-Control Frame

Before outlining or drafting, state compactly:

- **Promise:** the experience and central question owed to the reader.
- **Pressure source:** the person, system, relationship, scarcity, secret, or clock preventing an easy answer.
- **Change chain:** cause → decision → consequence → new constraint.
- **Thread states:** dormant, active, escalating, converging, paid, or intentionally deferred.
- **Information states:** what the reader, viewpoint character, allies, and opponents know or falsely believe.
- **Cost ladder:** what becomes harder, more public, more intimate, less reversible, or more morally expensive.
- **Resolution condition:** the decision and established mechanism capable of answering the promise.

Keep a distinction between facts, plans, and hypotheses. A plan in an outline is not yet an event in canon.

### 5. Design The Next-Chapter Contract

Give the chapter one primary job. Define:

- entry state and inherited emotional residue;
- viewpoint, location, world time, and elapsed time;
- immediate objective and opposition;
- active thread or promise being moved;
- information to expose, reinterpret, conceal legitimately, or pay off;
- one meaningful relationship or power shift;
- one irreversible or costly change;
- exit state and hook into the following chapter;
- details that must not change.

Use the chapter motion `inherit → pressure → choice → consequence → handoff`. Vary scene rhythm and emotional temperature inside that motion. Do not force a twist when a decision, recognition, or cost produces the stronger turn.

### 6. Run Pre-Draft Continuity Gates

Run the structural audit:

```bash
python3 .agents/skills/novel-story-telling/scripts/check_continuity.py --project-root .
```

Then perform the semantic gate using the context pack:

| Dimension | Entry fact | Proposed change | Evidence | Valid transition? |
| --- | --- | --- | --- | --- |
| Character knowledge |  |  |  |  |
| Physical state and possessions |  |  |  |  |
| Relationship and obligation |  |  |  |  |
| Location and elapsed time |  |  |  |  |
| World or genre rule |  |  |  |  |
| Clue, secret, or reveal |  |  |  |  |
| MacGuffin custody and meaning |  |  |  |  |
| Open thread and promised payoff |  |  |  |  |

Fix an invalid transition in the plan before drafting. If the author intends a retcon, identify every affected source file and obtain confirmation before changing established canon.

### 7. Draft Or Revise The Chapter

Follow the author-approved chapter contract and existing voice. Make every scene change at least one of: knowledge, leverage, relationship, objective, risk, resource, location, or commitment.

Preserve causal links. Use `therefore` or `but` transitions between major beats more often than unrelated `and then` transitions. Let relief expose consequences, deepen attachment, or reposition the next threat.

Do not hide information that the viewpoint character is actively thinking merely to manufacture surprise. Hide significance, access, motive, or interpretation instead.

For a new chapter, prepare a reviewed UTF-8 JSON payload. Use English field names and write `title`, `synopsis`, `draft`, and creative notes in the manuscript language:

```json
{
  "number": 7,
  "title": "The Burned Index",
  "slug": "the-burned-index",
  "status": "draft",
  "pov": "char-protagonist",
  "timeline": "Day 12, after sunset",
  "setting": "world-royal-archive",
  "word_target": 2500,
  "characters": ["char-protagonist"],
  "materials": [],
  "macguffins": ["macguffin-burned-index"],
  "plot_threads": ["plot-main"],
  "outline": "outline-chapter-007",
  "published": false,
  "tags": [],
  "synopsis": "One or two paragraphs describing the chapter's change.",
  "draft": "Complete manuscript prose.",
  "revision_notes": "Optional reviewed notes."
}
```

Write it with the bundled guardrail:

```bash
python3 .agents/skills/novel-story-telling/scripts/write_chapter.py \
  --project-root . \
  --input /tmp/chapter-007.json
```

The script must create exactly `chapters/NNN.lowercase-ascii-slug.md`, populate the repository chapter schema, and refuse any existing chapter number or path. Never bypass that refusal. If the number already exists, treat the task as a revision and edit that file minimally; do not regenerate or replace the whole file. Preserve its `created` date, set `updated` to the current ISO date, keep `number`, `id`, `title`, `slug`, filename, and H1 synchronized, and retain author text outside the requested revision.

Every chapter file must follow `chapters/_template.md` and contain exactly one H1 matching `title`, followed by exactly one each of `## Synopsis`, `## Draft`, and `## Revision Notes`. Put manuscript prose only in `## Draft`. Remove all template placeholder prose. Do not write a chapter outside `chapters/`, nest it in a subdirectory, omit YAML arrays, or invent non-ASCII filenames.

Treat the chapter file as an editorial container: only `## Draft` is
publishable. Keep Synopsis and Revision Notes useful to writers, but never
repeat their text as a preface, summary, or appendix inside Draft.

Use the Draft Markdown contract consistently:

- Use normal Markdown paragraph boundaries: only a blank line starts a new
  paragraph. Dialogue markup does not force a paragraph boundary.
- Keep narration as plain prose. Wrap every spoken range as exact `*“…”*`,
  whether it stands alone or shares a paragraph with narration, as in
  `*“Approved.”* Rhea said.` EPUB maps only that range to
  `<i class="dialog">` with serif italic styling.
- Reserve unquoted `*…*` for interior thought. Use curly single quotes `‘…’`
  for cited wording, remembered phrasing, or a quotation nested inside speech.
  A curly double-quoted span anywhere outside exact `*“…”*` markers is an error
  because it cannot be styled or classified safely.
- Use `**…**` only for genuine strong emphasis. Keep every marker pair balanced
  on one line.
- Use inline backticks only for literal machine output, UI labels, filenames,
  code identifiers, or log text.
- Put `---` alone between blank lines for a scene or time break. Never use
  `* * *` or a decorative bullet sequence.
- Do not use lists, blockquotes, or fenced code blocks anywhere inside Draft.
  Reserve H3 through H6 for genuine subheadings and do not add another H2 inside
  Draft.

Immediately after creating or revising the file, run:

```bash
python3 .agents/skills/novel-story-telling/scripts/check_continuity.py \
  --project-root . \
  --strict
```

Resolve every error. Review warnings and either fix them or report why they are intentional. Do not present a malformed chapter as completed.

The strict gate must reject curly double-quoted speech without the surrounding
emphasis and straight ASCII dialogue quotes. It must accept narration before or
after a marked dialogue range in the same paragraph, dialogue-only paragraphs,
unquoted italic interior thought, and curly single-quoted cited wording.

### 8. Post-Draft State Update

After the author accepts or finalizes a chapter:

1. Update source files for newly canonical character, world, plot, MacGuffin, or style facts.
2. Prepare a reviewed JSON fact card in the manuscript language:

```json
{
  "chapter": 12,
  "title": "Chapter title",
  "summary": "Objective account of what changed.",
  "canon_facts": [],
  "state_changes": [],
  "timeline_changes": [],
  "knowledge_changes": [],
  "macguffin_changes": [],
  "open_threads": [],
  "resolved_threads": [],
  "uncertainties": []
}
```

3. Preview the deterministic ledger change:

```bash
python3 .agents/skills/novel-story-telling/scripts/update_story_ledger.py \
  --project-root . --input /tmp/chapter-state.json --dry-run
```

4. After verifying every item against the chapter, rerun without `--dry-run`.
5. Rebuild the next chapter's context pack and rerun the continuity audit.

Never record speculation as a fact. Put ambiguity in `uncertainties` with competing interpretations.

## Token Discipline

- Use the ledger for stable outcomes and recent chapter excerpts for voice and immediate physical continuity.
- Retrieve by explicit source links before lexical relevance.
- Keep hard invariants even when they appear unrelated to the current scene.
- Trim prose before trimming rules, obligations, clue states, or character knowledge.
- Recompute context after an accepted chapter rather than carrying a stale chat summary forward.
- Treat token estimates as conservative approximations; inspect the generated pack size before expanding it.

## Completion Gate

Do not finish a story-planning or chapter task until:

- the target change advances the story promise or intentionally complicates it;
- escalation changes kind or cost, not only volume;
- the chapter exit differs materially from its entry;
- all used knowledge, rules, objects, and relationships have provenance;
- setups and payoffs remain tracked;
- the output language and prose style match the author's contract;
- structural audit errors are resolved;
- the chapter exists directly under `chapters/` with synchronized filename, frontmatter, H1, and required body sections;
- Draft prose follows the paragraph, dialogue, emphasis, literal-text, and
  scene-break Markdown contract;
- new canon is reflected in source files and the reviewed story ledger when applicable.
