# Analytical Review Modes

## Contents

1. Trigger matrix
2. Outline mode
3. Chapter mode
4. Manuscript mode
5. Regression mode
6. Fully autonomous start-to-publication handoff

## Trigger Matrix

| Request | Invoke analytical review? | Behavior |
| --- | --- | --- |
| Explicit outline, chapter, or manuscript critique/review | Yes | Review the requested scope; remain read-only by default |
| Explicit line editing or proofreading | Yes | Review only written text |
| Verification of earlier findings after revision | Yes | Run bounded regression mode |
| Fully autonomous writing from initial planning through publication | Yes | Inject manuscript review, disposition, revision, and regression before packaging |
| Ordinary planning, drafting, or revision without review language | No | Use the existing storytelling workflow |
| Ordinary publish, export, build, regenerate, package, or validate request | No | Use the existing publication workflow |
| Continuity or structural validation only | No | Use deterministic and semantic continuity checks |

`Review and publish` explicitly requests review, but it does not authorize
automatic revision. Present the review, then pass the unchanged manuscript to
the ordinary `publish-novel` preflight and packaging workflow. `Proofread and
fix` authorizes both phases; keep diagnosis and application distinct.

`Finish the remaining chapters and publish` does not by itself mean the author
delegated the complete lifecycle from initial planning. Do not infer the fully
autonomous trigger from ordinary completion or publication wording.

## Outline Mode

Review future direction without treating a plan as manuscript canon.

Evaluate:

- promise and governing question;
- cause, decision, consequence, and ownership;
- act, sequence, chapter, and beat functions;
- conflict differentiation and escalation dimensions;
- character motivation and state transitions;
- reader-model progression, reveal prerequisites, and information debt;
- setup, convergence, payoff, and resolution support;
- world rules, chronology, and constraint compatibility;
- whether exposition is attached to a planned action or decision.

Keep all three report sections. Limit line editing to the outline document's
own reference clarity, chronology, and causal wording. Explicitly defer prose
rhythm, dialogue quality, diction, and scene-level sentence judgment until a
Draft exists.

Do not turn critique into unrequested ideation. Any new plot direction remains
a proposal, not canon.

## Chapter Mode

Review the explicitly named chapter or chapters. Read relevant project and
continuity sources to understand intent, then ground reader-effect claims only
in publishable Draft text.

Check the chapter's entry and exit state, primary job, causal motion,
information progression, character agency, cost, and handoff. Review local
prose only after chapter-level structure and information order.

Do not generalize a chapter-level issue to the entire work unless other
chapters have been inspected and provide independent evidence.

## Manuscript Mode

Run the inventory helper and inspect every eligible numbered chapter:

```bash
python3 "<skill-dir>/scripts/inventory_review.py" \
  --project-root . \
  --mode manuscript \
  --max-batch-tokens 12000
```

The printed inventory contains metadata, hashes, line ranges, token estimates,
and batches, but no manuscript prose. Stop short of a complete-coverage claim
when it reports an invalid or empty Draft.

Review bounded units in filename order. Maintain a working coverage table,
unit findings, strengths, open questions, and cross-unit evidence. Synthesize
whole-work patterns only after all units are reviewed. A unit with no finding
must still appear as reviewed.

Do not flatten the complete manuscript into one prompt merely for convenience.
If one chapter exceeds the batch budget, review it as its own unit or split it
at stable scene/subheading boundaries while preserving one chapter-level
result.

## Regression Mode

Regression review accepts prior finding IDs and their dispositions:

```yaml
findings:
  - id: W1
    disposition: apply | defer | reject
    rationale:
    changed_units: []
```

Review applied high-impact findings first, then their structural dependencies
and changed or adjacent units. Limit new findings to regressions introduced by
the revision or directly related issues that prevent verification.

Do not reopen deferred or rejected findings unless their evidence materially
changed. Do not start another unrestricted critique pass. By default, perform
one focused regression pass and report:

- resolved findings;
- unresolved findings;
- introduced regressions;
- deferred or rejected findings left closed;
- any decision that still requires the author.

The reviewer remains read-only. Apply changes through `novel-story-telling`
only when separately authorized.

## Fully Autonomous Start-To-Publication Handoff

Only an explicit request delegating the complete novel lifecycle from initial
planning through publication authorizes automatic review and revision.

After all chapters are drafted:

1. Run manuscript-mode analytical review.
2. Record `apply`, `defer`, or `reject` for each material finding with a concise
   rationale.
3. Apply selected findings through `novel-story-telling`.
4. Update canon and the story ledger as required.
5. Run one bounded regression review.
6. Resolve material regressions that can be corrected within the authorized
   scope.
7. Run strict continuity validation.
8. Invoke `publish-novel` for deterministic EPUB packaging.

Do not make `build_epub.py` or an ordinary `publish-novel` request responsible
for literary judgment. Deferred or rejected findings belong in the handoff,
not in the EPUB validator.
