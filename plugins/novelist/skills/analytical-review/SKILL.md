---
name: analytical-review
description: Review novel outlines, drafted chapters, full manuscripts, and prior revision findings as an independent analytical editor. Use when the author explicitly requests critique, developmental review, work examination, line editing, proofreading, whole-manuscript review, or regression verification, and when an explicitly fully autonomous workflow covers the complete novel lifecycle from initial planning through publication. Produce an intent-aware, evidence-backed report with Overall Assessment, Work Examination, and Line Editing or Proofreading sections while remaining read-only by default. Do not invoke this skill automatically for ordinary planning, drafting, revision, continuity validation, EPUB export, build, regeneration, packaging, validation, or publication requests.
---

# Analytical Review

Before running a bundled command, resolve `<skill-dir>` to the absolute
directory containing this `SKILL.md`. Keep `--project-root` pointed at the
active novel workspace, not at the skill or plugin installation.

## Operating Contract

Adopt an independent reviewer role. Diagnose the work without changing it.
Do not edit outlines, chapters, canon, the story ledger, or generated output
during a review-only request.

If the author requests both review and revision, finish and present the
diagnosis before applying selected findings. Use `novel-story-telling` for the
revision phase and preserve finding IDs across the handoff.

Write all internal instructions, temporary schemas, and script inputs in
English. Return the review in this order of precedence:

1. the language explicitly requested by the author;
2. `project.md` `language`;
3. `style/000.style-guide.md` `language`;
4. the dominant language of the reviewed source.

Localize report headings naturally while preserving the semantic section order
defined in [report-contract.md](references/report-contract.md). For Korean
output, use the canonical labels `작품 총평`, `작품 검토`, and `문면 교열`.

Treat the current manuscript and review response as private runtime material.
Use relative source anchors and only the shortest excerpt needed for evidence.
Do not copy manuscript prose or review output into the project, plugin,
examples, fixtures, or generated package. Save a report only when the author
explicitly requests a file and confirms its destination.

## 1. Confirm Authorization, Mode, And Scope

Read [review-modes.md](references/review-modes.md). Select exactly one mode:

- `outline`: planned story direction before prose exists;
- `chapter`: one or more explicitly named Drafts;
- `manuscript`: every numbered publishable chapter plus cross-chapter synthesis;
- `regression`: bounded verification of earlier findings after revision.

Invoke this skill only when:

- the author explicitly requests review, critique, line editing, proofreading,
  developmental feedback, or verification of prior findings; or
- the author explicitly delegates the complete autonomous lifecycle from
  initial planning through final publication.

Do not infer review authorization from an ordinary planning, drafting,
revision, validation, export, build, package, or publish request. `Review and
publish` authorizes review but not automatic revision. `Proofread and fix`
authorizes both phases; keep them distinct.

Confirm the requested source scope. For a chapter request, identify exact
chapter numbers or relative paths. For regression mode, require the prior
finding IDs, dispositions, and changed units.

## 2. Orient To The Work

Read:

- `AGENTS.md`;
- `project.md`;
- `style/000.style-guide.md`;
- `plot/000.master-plot.md`;
- `outlines/000.master-outline.md`;
- the sources in the declared review scope;
- only the linked character, world, material, MacGuffin, and plot files needed
  to establish intent or continuity.

Do not load every source file by default. Use author-side sources to understand
intent, rules, and hidden truth. Use only publishable `## Draft` text to claim
that a reader knows, sees, or can infer something.

Resolve conflicting evidence by the project authority order: explicit author
direction > `final` source > `revision` source > latest manuscript fact >
`draft` source > outline or seed. Keep unresolved conflicts visible.

## 3. Inventory The Review Scope

Use the bundled content-free inventory helper before reading findings into a
whole-work conclusion.

For outline review:

```bash
python3 "<skill-dir>/scripts/inventory_review.py" \
  --project-root . \
  --mode outline
```

Add one or more `--target outlines/<file>.md` or `--target plot/<file>.md`
options when the author selected a narrower plan.

For chapter review:

```bash
python3 "<skill-dir>/scripts/inventory_review.py" \
  --project-root . \
  --mode chapter \
  --chapter <number>
```

For manuscript review:

```bash
python3 "<skill-dir>/scripts/inventory_review.py" \
  --project-root . \
  --mode manuscript \
  --max-batch-tokens 12000
```

The command prints relative paths, metadata, line ranges, hashes, estimates,
and batches without copying prose. Prefer this non-persistent output. If an
external file is explicitly needed, pass a fresh, non-existing `--output`
path; the helper creates it exclusively with private permissions and refuses
collisions. Stop short of a complete-coverage claim when `coverage_complete`
is false. Do not omit a valid numbered chapter because it appears unlikely to
produce feedback.

## 4. Build The Review Charter

Read [review-method.md](references/review-method.md). Before producing findings,
record:

- mode, scope, form, genre, point of view, style, and completion stage;
- work promise, intended reader experience, and target-reader assumptions;
- project constraints;
- protected techniques and the boundary of each protection;
- work-specific review axes;
- limitations and unresolved premises;
- any external research required to avoid a material false positive.

Derive axes from this work rather than forcing a universal checklist. Protect
an intentional device from generic correction while still testing whether each
instance performs its intended function.

Use external research only when it can materially change a finding. Prefer
primary sources and separate external evidence from manuscript evidence. Do not
browse merely to decorate the report.

## 5. Review Bounded Units

Read each eligible inventory unit in order. For a full manuscript, use the
inventory batches, but keep one result per chapter or stable bounded span.
Track:

- reviewed unit and Draft line range;
- evidence-backed strengths;
- work findings and line findings;
- open questions and unresolved premises;
- candidate cross-unit patterns;
- active, revised, or withdrawn review axes.

Mark a unit reviewed even when it has no material finding. Complete all unit
passes before synthesizing whole-work tendencies.

Test patterns with deterministic search when useful. A global tendency requires
multiple independent evidence locations. Keep a single local issue local.
Withdraw or revise a hypothesis when the complete available work disproves it.

In outline mode, evaluate planned causality, unit function, motivation,
reader-model progression, setup/payoff, constraints, and direction. Do not
claim defects in unwritten dialogue, diction, rhythm, or scene prose.

In regression mode, verify prior material findings and affected dependencies.
Limit new findings to revision regressions or directly related blockers. Do not
reopen deferred or rejected findings without materially changed evidence, and
do not begin another unrestricted review.

## 6. Write The Report

Read [report-contract.md](references/report-contract.md). Lead with:

1. Overall Assessment;
2. Work Examination;
3. Line Editing / Proofreading.

Localize those headings in the output language. For Korean, use `작품 총평`,
`작품 검토`, and `문면 교열`. Keep their semantic order.

Distinguish observation, interpretation, confidence, reader effect, and
suggested direction. Use stable `W1` and `L1` style IDs. Present minimal
revision options rather than a replacement manuscript.

Do not force a finding count. State when no material finding exists. Put
structural dependencies before dependent line edits in the revision order.

For manuscript mode, append a compact coverage table and compare its reviewed
unit set with the inventory. Do not claim whole-manuscript completion unless
every eligible unit appears and the inventory has no blocking issue.

The optional method appendix may summarize the charter, sources, limitations,
and withdrawn axes. Do not expose hidden chain-of-thought.

## 7. Handle The Handoff

For a review-only request, stop after the report and wait for the author to
select findings or request revision.

For an explicit review-and-publish request that does not authorize revision,
present the report, leave all literary findings unapplied, and then hand the
unchanged manuscript to `publish-novel` for its existing structural and
continuity preflight plus deterministic packaging. Literary findings do not
become build failures.

For an explicitly authorized review-and-fix request:

1. preserve finding IDs and author dispositions;
2. apply only selected changes through `novel-story-telling`;
3. update canonical sources and the story ledger as required;
4. run one focused regression review unless the author requests broader work.

For a fully autonomous start-to-publication request, follow the bounded
handoff in [review-modes.md](references/review-modes.md): manuscript review,
`apply`/`defer`/`reject` disposition, story revision, one focused regression
pass, strict continuity validation, then deterministic `publish-novel`
packaging.

Never inject this loop into an ordinary publication request. Deferred or
rejected literary findings are handoff state, not EPUB validation errors.

## Completion Gate

Do not finish until:

- the mode and source scope are explicit;
- the charter records protected techniques, axes, limitations, and uncertainty;
- reader-effect claims use reader-visible Draft evidence;
- every unit in scope has been inspected;
- full-manuscript coverage matches the deterministic inventory;
- strengths and recurring tendencies have evidence;
- outline review defers unwritten prose judgments;
- observations, interpretations, and revision options remain distinguishable;
- the report contains the three localized semantic sections in order;
- structural dependencies precede dependent line edits;
- review-only work left source files unchanged;
- no manuscript or review output was persisted without explicit authorization.
