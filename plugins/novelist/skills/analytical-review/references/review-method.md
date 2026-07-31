# Analytical Review Method

## Contents

1. Editorial stance
2. Review charter
3. Protected techniques
4. Evidence layers
5. Review axes
6. Full-scope verification
7. Research
8. Final audit

## Editorial Stance

Reconstruct the work's intended reading contract before judging execution. The
review should help this work become more fully itself, not normalize it into a
generic model of prose or plot.

Evaluate function and reader effect:

- what the reader can perceive, connect, infer, question, or misread;
- what a scene, chapter, sequence, or sentence changes;
- who owns a decision or consequence;
- whether a rule, reveal, reversal, or ending has recoverable preparation;
- whether local wording interrupts the intended reading speed or reference.

Prefer the smallest repair that restores the intended effect. Preserve voice,
genre convention, productive ambiguity, open endings, and deliberate
difficulty. Do not infer a defect from personal taste alone.

## Review Charter

Build this compact charter before producing findings:

```yaml
mode: outline | chapter | manuscript | regression
scope: []
form:
genre:
point_of_view:
style:
completion_stage:
work_promise:
intended_reader_experience:
target_reader:
project_constraints: []
protected_techniques: []
review_axes: []
limitations: []
unresolved_premises: []
external_research: []
```

Derive the charter from `project.md`, the style guide, relevant plot and
outline sources, and the source being reviewed. Keep facts, author plans, and
editorial hypotheses distinct.

The author-facing response may summarize this charter as an audit appendix.
Do not expose hidden chain-of-thought or private intermediate reasoning.

## Protected Techniques

Record each protected technique with:

- the technique;
- evidence that it is intentional or structurally established;
- the function it is meant to perform;
- what must not be "corrected" merely for being unconventional;
- the boundary at which local execution may still be reviewed.

Protection is not immunity. A recurring device may be intentional while one
instance arrives too early, repeats an already learned code, obscures a
reference, or weakens a later beat. Critique that local function without
rejecting the device itself.

## Evidence Layers

Keep these layers separate:

| Layer | Contents | Permitted use |
| --- | --- | --- |
| Project contract | Author instructions, style, genre, constraints | Establish intent and review boundaries |
| Author truth | Canon, hidden mechanisms, future plans | Check consistency; never count as reader exposure |
| Viewpoint model | What a viewpoint character knows or believes | Use only when Draft makes it available |
| Reader evidence | What publishable Draft has shown or stated | Basis for reader-knowledge and inference claims |
| Expected inference | What a defined target reader may conclude | Editorial hypothesis; attach confidence |
| External source | Primary research used to prevent a false positive | Cite separately from manuscript evidence |

For every material finding, distinguish:

- **observation:** what is present in the source;
- **interpretation:** how it may function in context;
- **reader effect:** the concrete reading consequence;
- **confidence:** `confirmed`, `likely`, or `unresolved`;
- **suggested direction:** one or more minimal options, not a mandatory rewrite.

Strengths also require evidence. Do not claim a recurring tendency from one
local instance. Do not use `throughout`, `consistently`, or an equivalent
whole-work term until multiple independent locations have been checked.

## Review Axes

Derive axes from this work's promise and risks. Candidate axes include:

- reader inference space and information timing;
- causal ownership of off-stage or mediated actions;
- viewpoint boundaries and unsupported certainty;
- conflict function across acts, sequences, chapters, or scenes;
- cost and consequence carried into the next unit;
- exposition attached to current action and decision;
- character agency under rules or constraints;
- setup, reinforcement, payoff, and resolution preparation;
- chronology, terminology, object custody, and state continuity;
- sentence-level reference, order, parallelism, duplication, and rhythm.

Candidates are not a mandatory checklist. For each selected axis record:

```yaml
name:
review_question:
failure_risk:
contract_comparison:
evidence_needed:
status: active | revised | withdrawn
```

Withdraw or revise an axis when full-scope inspection disproves its premise.
Do not preserve a finding merely because it appeared in an early hypothesis.

## Full-Scope Verification

Read every source unit in the declared scope. Use deterministic search when it
can verify distribution, distance, chronology, terminology, speaker
attribution, repeated action, rule invocation, setup/payoff, or information
arrival.

For manuscript review:

1. Inventory every numbered chapter using the bundled helper.
2. Review reader effects from each chapter's `## Draft` only.
3. Mark each eligible unit reviewed even when it produces no finding.
4. Finish unit reviews before cross-chapter synthesis.
5. Require independent evidence locations for a global pattern.
6. Do not claim complete coverage while an eligible unit remains unreviewed or
   the inventory reports a malformed Draft.

Use Synopsis, Revision Notes, outlines, and source sheets to understand author
intent and continuity. Never treat them as proof that the reader has seen a
fact.

## Research

Research only when a genre, historical, scientific, cultural, or language fact
could materially change a finding. Prefer primary sources and current
authoritative references. Record:

- the question being checked;
- the source and access date when relevant;
- the conclusion that affects the review;
- the remaining uncertainty.

Do not browse merely to decorate the report. Do not let external convention
override an explicit project contract without identifying the conflict.

## Final Audit

Before delivering the report, verify:

- every finding matches the declared scope and mode;
- protected techniques were not criticized merely for existing;
- observations, interpretations, and suggestions are distinguishable;
- uncertainty is not presented as fact;
- strengths and global tendencies have evidence;
- outline review does not invent prose-level defects;
- revision order places structural dependencies before dependent line edits;
- suggestions preserve the work's voice and intended ambiguity;
- the report contains no fixed quota of findings;
- no source text was written into the project or plugin repository.
