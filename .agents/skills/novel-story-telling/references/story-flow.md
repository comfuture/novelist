# Story Flow And Conflict Control

## Contents

1. Reader contract
2. Causal architecture
3. Pressure and release
4. Thread control
5. Reveal control
6. Chapter and scene engines
7. Resolution design
8. Continuity state
9. Failure modes

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
