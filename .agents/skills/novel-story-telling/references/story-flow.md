# Story Flow And Conflict Control

## Contents

1. Reader contract
2. Reader mental-model control
3. Causal architecture
4. Pressure and release
5. Thread control
6. Reveal control
7. Chapter and scene engines
8. Resolution design
9. Continuity state
10. Failure modes

## Reader Contract

Define the promise as an experience plus a question, not merely a premise. Examples:

- witness a powerless outsider learn what justice costs;
- discover how an impossible crime was performed;
- watch a family choose between truth and belonging;
- explore whether a beneficial technology can remain humane.

Track how each major unit serves the promise:

| Unit | Question sharpened | Pressure added | Choice forced | Promise advanced |
| --- | --- | --- | --- | --- |
| Act or sequence |  |  |  |  |
| Chapter cluster |  |  |  |  |
| Chapter |  |  |  |  |

If a unit does not change the reader's question, character's options, or cost of action, compress, combine, or remove it.

## Reader Mental-Model Control

Treat the reader model as an explicit editorial hypothesis about a defined target reader, not as a claim about every reader's actual mind. Specify the target reader's assumed language, genre literacy, remembered story anchors, and tolerance for unfamiliar terms. Do not solve ambiguity by silently assuming an expert reader unless the project establishes one.

### Keep evidence layers separate

| Layer | Contents | Count as reader knowledge? |
| --- | --- | --- |
| Author truth | Canon, backstory, future events, hidden mechanisms | No |
| Viewpoint model | What the viewpoint character knows, believes, or avoids | Only when Draft makes it available |
| Reader evidence | What prior and current Draft text has shown or stated | Yes |
| Expected inference | What the target reader will probably conclude from that evidence | Editorial hypothesis; verify |

Never infer reader knowledge from Synopsis, Revision Notes, outlines, source sheets, or hidden-truth fields. When reader and viewpoint knowledge differ, make the asymmetry deliberate and reader-recoverable.

### Map the state trajectory

Before drafting a chapter, define its entry and exit reader models. For every scene or major turn, fill this compact map:

| Beat or scene | Entry model | Recalled anchor | Reader-visible cue | Intended update or inference | Deliberately unresolved | Exit question or prediction |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Prefer one primary conceptual update per beat. A beat may move several plot states, but the reader should have a dominant change to integrate: learn a fact, revise a cause, revalue a person, recognize a pattern, or replace a governing question.

Use this cohesion test between adjacent beats:

> Because the reader has seen **X**, they can interpret **Y** as **Z**; therefore the next beat changes **Q**.

If the sentence cannot be completed without author-only information, add a reader-facing prerequisite, reorder the beats, or change the intended inference.

### Layer information for comprehension and reward

- Move from a recalled anchor to a new observation, then to implication and consequence.
- Separate what is observed, how a character interprets it, what the reader may infer, and what is actually true.
- Introduce a name, rule, location, or device before its exact identity matters, or attach it immediately to a familiar function, desire, threat, or contrast.
- Let the reader use a new model in a decision, prediction, or reinterpretation before adding another dense model.
- After action or a reveal, include enough consequence or reflection for the reader to update the larger picture.
- Withhold truth, motive, significance, or access when useful; do not withhold basic scene orientation merely to create mystery.
- Preserve inference as a source of pleasure. Do not explain a connection that the Draft has made legible unless the voice, character, or genre calls for confirmation.

Treat every unexplained term, unnamed causal gap, and unresolved reference as information debt. Debt can create curiosity, but several unrelated debts introduced together create fog. Flag a beat for revision when it requires the reader to integrate three or more unrelated new entities, rules, time frames, or causal claims before any one becomes usable.

### Audit from the reader side

After drafting, ignore author-side sources and reconstruct the trajectory from publishable Draft text. At each checkpoint, complete these sentences in one line each:

- The reader can now describe ...
- The reader likely believes or suspects ... because ...
- The reader still asks ...
- The reader anticipates ...
- The intended feeling arises from ...

Compare the reconstruction with the planned map. Classify mismatches before revising:

- **missing anchor:** identity, location, goal, time, or stakes cannot be recovered;
- **causal leap:** the intended conclusion lacks a visible premise;
- **author-knowledge leak:** prose assumes a source-only fact;
- **orphan detail:** information has no current function or memorable attachment;
- **overload:** several unrelated updates compete in one beat;
- **accidental false model:** cues strongly support an unintended conclusion;
- **stagnation:** repetition adds words but does not confirm, complicate, or reframe;
- **over-explanation:** prose states the connection after the reader has already earned it.

Repair the smallest broken link. Prefer changing sequence, adding a concrete cue, attaching a detail to an existing anchor, splitting a beat, or deleting noise. Add exposition only when the missing link itself must be stated.

### Persist across chapters

In the story ledger, keep reader-facing evidence separate from expected inference and open questions. Reader-facing evidence is verifiable against Draft; expected inference is editorial and may be wrong; an open question is intentional only when the chapter supplies enough orientation to formulate it. Recheck the latest reader-model entry against prior Draft before using it as the next chapter's baseline.

## Causal Architecture

Use a flexible macro path:

1. **Charged equilibrium:** show the bargain or belief holding the current life together.
2. **Disruption:** make the old bargain insufficient.
3. **Commitment:** force an action that closes the easy return path.
4. **Expansion:** reveal more actors, systems, histories, and consequences.
5. **False model or false victory:** let progress expose a deeper error.
6. **Convergence:** collide external pressure, internal need, and relationship obligation.
7. **Crisis choice:** remove the option to satisfy every value.
8. **Climax:** resolve through established means and protagonist agency.
9. **Aftermath:** show the new state and the price that remains.

This is a control map, not a mandatory act count. Move or repeat stages when the genre contract requires it.

At each major turn, verify:

- the cause is visible or recoverable;
- the character's response follows their knowledge and values;
- the response creates a consequence;
- the consequence changes the next decision space.

## Pressure And Release

Escalate by changing dimensions:

- **time:** deadline shortens or opportunity closes;
- **scope:** private issue affects family, faction, institution, or world;
- **intimacy:** conflict reaches a more valued relationship or identity;
- **publicity:** private failure becomes witnessed, recorded, or reputational;
- **dependency:** the needed ally, resource, or system becomes less replaceable;
- **knowledge:** a new truth invalidates the current plan;
- **agency:** available choices narrow or become mutually exclusive;
- **moral cost:** success requires a value violation or sacrifice;
- **irreversibility:** recovery becomes expensive, partial, or impossible;
- **adaptation:** opposition learns from the protagonist's last tactic.

Do not raise every dimension at once. Select one primary and one secondary dimension per escalation beat so later turns retain room.

Use release beats to:

- expose the cost of the previous crisis;
- let characters interpret events differently;
- deepen attachment that a later choice can endanger;
- transfer resources, knowledge, or status;
- permit a partial success that opens the next problem;
- restore reader orientation after dense action or revelation.

Relief without state change is expendable. Constant intensity flattens perceived intensity.

## Thread Control

Give every plot thread a compact state card:

```yaml
thread_id:
promise:
owner:
opposition:
current_state: dormant | active | escalating | converging | paid | deferred
last_change:
next_pressure:
required_setup: []
payoff_condition:
deadline_or_window:
linked_threads: []
```

Apply these rules:

- Keep the main thread visible through consequence even when another thread dominates a chapter.
- Revive a dormant thread with a changed implication, not a repeated reminder.
- Converge threads when one action changes two or more promises.
- Defer intentionally by recording the reason and next viable window.
- Pay a promise with proportional narrative weight.
- Distinguish closure from cessation: a threat can stop without answering what it meant.

## Reveal Control

Separate four states:

1. the truth;
2. available evidence;
3. each character's belief;
4. what the reader has been shown.

For every major reveal, record:

```yaml
reveal_id:
truth:
surface_model:
seed_evidence: []
reinforcement: []
misdirection_with_cause: []
reader_exposure:
character_exposure:
reframe_point:
payoff_consequence:
```

Prefer the sequence `expose → normalize or misread → contradict → reframe → force choice`. The reveal matters when it changes action, allegiance, danger, or meaning. Do not place several unrelated reveals back-to-back without allowing behavior to change.

Withhold significance rather than observable facts. A red herring must arise from an actual motive, process, mistake, or secret.

## Chapter And Scene Engines

### Chapter contract

Specify:

- entry state;
- primary objective;
- active opposition;
- governing uncertainty;
- pressure increase;
- decision or recognition;
- irreversible change;
- exit state;
- next-chapter affordance.

Useful chapter roles include pursuit, test, revelation, reversal, aftermath, alliance, fracture, preparation, sacrifice, and decision. Avoid repeating the same role and emotional shape without a purposeful pattern.

### Scene engine

Use:

1. objective;
2. obstacle or incompatible objective;
3. tactic;
4. resistance;
5. tactic change;
6. turn;
7. consequence;
8. exit question.

Scene tension can come from subtext, incomplete information, spatial constraint, competing duties, resource scarcity, status risk, time, or bodily vulnerability. Action is only one form.

### Scene audit

Ask:

- What changes because this scene exists?
- Why must it happen now and here?
- Why can the viewpoint character not leave unchanged?
- Which detail is setup, proof, pressure, or payoff?
- What emotional residue enters the next scene?

## Resolution Design

Build the ending backward from the promise. A strong resolution aligns:

- an established external mechanism;
- a protagonist decision unavailable to their earlier self;
- a cost proportional to the conflict;
- a payoff to important setup;
- a visible new state.

Resolution patterns:

- exploit a previously demonstrated constraint;
- combine two established rules or relationships;
- reinterpret the goal after recognition;
- trade victory in one dimension for loss in another;
- expose a hidden truth and accept its social cost;
- redesign an institution or bargain rather than defeat one person;
- choose separation, forgiveness, punishment, containment, or coexistence;
- achieve local closure while acknowledging systemic remainder.

Do not use an unseeded exception, sudden confession, accidental rescue, or newly introduced power to solve the governing conflict.

## Continuity State

Track stable state separately from prose summaries:

- character location, condition, inventory, ability, knowledge, desire, and allegiance;
- relationship trust, debt, intimacy, resentment, dependency, promises, and public status;
- world rules, costs, exceptions, institutions, and resource conditions;
- timeline events, elapsed time, travel, season, and deadlines;
- clues, evidence, secrets, witnesses, and interpretations;
- MacGuffin location, custody, surface meaning, true function, and reveal stage;
- thread promise, last movement, next pressure, and payoff state.

Record state transitions as `before → cause → after`. Preserve uncertainty explicitly.

## Failure Modes

- Escalation means only larger fights, louder arguments, or higher body counts.
- Chapters contain events but no changed decision space.
- Summaries preserve plot events but lose knowledge, promises, injuries, or object custody.
- An outline plan is treated as if it already happened.
- Characters know facts unavailable to them.
- A surprise depends on unnatural viewpoint omission.
- A setup is mentioned repeatedly but never changes meaning.
- A resolution answers mechanics but not the moral, emotional, or thematic question.
- The aftermath restores the old equilibrium without addressing the cost.
- Genre devices override the project's established voice or reader contract.
