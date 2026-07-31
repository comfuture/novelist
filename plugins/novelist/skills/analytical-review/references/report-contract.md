# Analytical Review Report Contract

## Contents

1. Language and ordering
2. Overall assessment
3. Work examination
4. Line editing and proofreading
5. Coverage appendix
6. Finding discipline

## Language And Ordering

Return the report in the selected author-facing language. Localize headings
naturally, but preserve these semantic sections and order:

1. `overall_assessment`
2. `work_examination`
3. `line_editing`

For Korean output, use these canonical top-level labels in that order:

1. `작품 총평`
2. `작품 검토`
3. `문면 교열`

An optional coverage and method appendix may follow these sections. Never put
research notes or planning material before the main feedback.

## Overall Assessment

Include four subsections:

### How The Work Was Read

Describe form, point of view, central pressure, governing devices, and ending or
planned resolution strategy. Explain the design you evaluated; do not retell
the plot.

### What Is Working

Connect each strength to evidence and a reader-facing or structural function.
Avoid generic praise.

### Recurring Tendencies

Group only findings supported by multiple independent instances. Cite the
related finding IDs. If there is no supported pattern, say so briefly rather
than manufacturing one.

### Revision Order

Order work by impact, dependency, and revision cost. Put structural findings
before line edits that may be invalidated by structural changes. This is an
editing sequence, not an absolute verdict on quality.

## Work Examination

Use stable IDs such as `W1`, `W2`, and `W3`. Include:

```yaml
id:
category:
title:
scope:
confidence: confirmed | likely | unresolved
observation:
evidence_anchors: []
context:
protected_intent:
reader_effect:
why_it_matters:
revision_options: []
related_findings: []
structural_dependencies: []
```

Use relative source paths plus section, scene, beat, or line anchors. Include
only the shortest excerpt needed when an anchor alone is insufficient.

Frame revision options as choices. Do not silently rewrite the passage or
invent new canon.

## Line Editing And Proofreading

Use stable IDs such as `L1`, `L2`, and `L3`. Include:

```yaml
id:
category:
location:
confidence: confirmed | likely | unresolved
issue:
reread_trigger:
local_effect:
minimal_options: []
structural_dependency:
```

Possible categories include terminology or reference drift, nearby repetition,
action/decision/execution order, subject or modifier ambiguity, parallel
structure, duplicated information, speaker attribution, chronology deixis,
spelling, punctuation, and sentence rhythm.

Separate factual grammar or spelling errors from stylistic preference. Defer a
line edit when a structural revision may remove or replace the passage.

In outline mode, keep this section but review only the outline document's own
reference precision, chronology, and causal wording. State that prose rhythm,
dialogue, diction, and scene-level line editing remain deferred until Draft.

## Coverage Appendix

For a full manuscript, end with a compact coverage table:

| Unit | Reviewed source | Status | Finding IDs |
| --- | --- | --- | --- |
| Chapter or bounded span | Draft line range | reviewed | IDs or `none` |

Compare the reviewed-unit set with the deterministic inventory. Do not claim
complete coverage unless every eligible inventory unit appears in this table
and the inventory has no blocking issue.

The appendix may also summarize:

- review mode and scope;
- protected techniques;
- active, revised, and withdrawn axes;
- limitations and unresolved premises;
- external sources that materially affected a finding.

Keep this an inspectable method summary, not a transcript of hidden reasoning.

## Finding Discipline

- Do not target a fixed number of findings.
- Do not repeat one problem in both detailed sections unless the line finding
  is a distinct local manifestation with a dependency link.
- Prefer one finding with several evidence anchors over several duplicate
  findings.
- Preserve uncertainty when author intent or causal meaning is not recoverable.
- State when a section has no material finding.
- Make the report useful for revision without requiring the author to accept
  every suggestion.
