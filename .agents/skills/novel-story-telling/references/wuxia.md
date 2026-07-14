# Wuxia Story Design

## Contents

1. Genre contract
2. Story engine
3. Recommended flow
4. Escalation and resolution
5. Scene devices
6. Continuity ledgers
7. Failure modes
8. Research basis

## Genre Contract

Treat `xia` as an ethical position tested through action: personal loyalty, justice, freedom, altruism, and resistance to corrupt hierarchy can conflict with one another. Treat `jianghu` as a social field with reputation, factions, debts, unofficial law, and consequences beyond formal government.

Do not reduce wuxia to numeric advancement. Martial capability matters because it changes what a character can protect, refuse, expose, or destroy. Every important gain should enlarge obligation, visibility, temptation, or cost.

## Story Engine

Choose at least two valid duties that cannot both remain intact:

- loyalty to a benefactor vs justice for a victim;
- sect obedience vs personal moral judgment;
- vengeance vs protection of innocents;
- family duty vs sworn fellowship;
- preservation of a lineage vs preventing its abuse;
- court law vs jianghu justice;
- truth about a mentor vs gratitude owed to that mentor;
- freedom from obligation vs responsibility created by power.

Define the protagonist's initial interpretation of righteousness. Build turns that expose the limitations of that interpretation. The climax should test the revised code through a martial and ethical choice at the same time.

## Recommended Flow

1. **Uneasy order**
   Establish daily life, a skill limitation, one gratitude debt, one grievance or oath, and a distorted belief about justice.
2. **Injustice or summons**
   Use a killing, accusation, stolen manual, broken oath, threatened community, or request from a benefactor to force entry into wider jianghu.
3. **First crossing**
   Let a local success make the protagonist visible to rivals, officials, sects, witnesses, or creditors. Convert success into obligation.
4. **Network expansion**
   Introduce factions through incompatible claims on a person, technique, artifact, territory, testimony, or historical event.
5. **Partial mastery and moral failure**
   Grant a technique, ally, or reputation advantage. Let the protagonist misuse it because revenge, obedience, face, or loyalty is mistaken for righteousness.
6. **Hidden history**
   Reframe a mentor, lineage, massacre, manual, succession, or political conflict. Change both the debt map and the meaning of justice.
7. **Debt collision**
   Force two legitimate duties into direct conflict. Remove the possibility of solving both by superior fighting alone.
8. **Martial and ethical climax**
   Make the decisive technique or refusal embody the protagonist's chosen code.
9. **Jianghu aftermath**
   Settle, transfer, forgive, expose, or deliberately defer major debts. Show the new reputation, faction balance, lineage access, and effect on ordinary people.

## Escalation Devices

- **Debt collision:** fulfilling one life debt violates another oath.
- **Reputation cascade:** rumor changes lodging, prices, witnesses, recruitment, marriage, and faction responses before the hero can answer it.
- **Face ladder:** private insult → witnessed challenge → faction duty → inter-sect conflict.
- **Sect contradiction:** doctrine demands one action while institutional survival demands another.
- **Technique cost:** power requires injury, secrecy, forbidden lineage, a specific terrain, emotional state, or moral compromise.
- **Inheritance contest:** multiple claimants have legitimate rights to a manual, weapon, title, or testimony.
- **Authority squeeze:** court and outlaw power each offer incomplete justice.
- **False master:** a teacher's facts are accurate but their moral framing serves hidden interests.
- **Assembly inversion:** a tournament or summit is actually a legitimacy trial, recruitment trap, assassination cover, or witness harvest.
- **Rescue debt:** saving someone creates a claimant or public obligation instead of resetting tension.
- **Counter-technique revelation:** an opponent exposes a hidden limitation and forces tactical as well as ethical adaptation.
- **Succession fracture:** choosing an heir destabilizes relationships, doctrine, and faction control.

Vary escalation across martial danger, reputation, debt, institutional stakes, intimate loyalty, and moral irreversibility.

## Resolution Devices

- Pay off a seeded martial constraint and ethical premise through the same action.
- Distinguish punishment, exposure, forgiveness, restitution, and cycle-breaking in revenge resolutions.
- Let victory cost status, bodily capacity, lineage access, a relationship, or legal freedom when the story promises sacrifice.
- Resolve institutional conflict through leadership change, public testimony, doctrinal reform, separation, or fragile balance, not only the defeat of a stronger fighter.
- Let mercy create a future obligation rather than erase consequences.
- Show how villagers, disciples, servants, or travelers experience the new order.

## Scene Devices

### Teahouse or inn

Deliver rumor, faction geography, reputation shifts, coded threats, and conflicting versions of history. Give each speaker a reason to distort the account.

### Courtesy duel

Use ritual politeness to negotiate rank, debt, identity, and allegiance. Track who issues the challenge, who witnesses it, the accepted conditions, and what refusal would mean.

### Technique tell

Use footwork, breathing, scars, calluses, wound patterns, weapon maintenance, or damage to infer lineage or concealed identity. Seed the tell before making it decisive.

### Training

Make training correct a misconception, expose a limitation, deepen a bond, or create a cost. Do not use it solely for rank increase.

### Oath

Record exact wording, scope, witnesses, loopholes, penalty, and who interprets it differently.

### Duel progression

Use `probe → identify school → test constraint → reveal motive → incur cost → make moral choice`. Each exchange should change information or options.

### Chapter hook

Prefer a changed debt, inferred identity, compromised oath, betrayal obligation, faction claim, or impossible duty over an unrelated attack.

## Continuity Ledgers

### Debt

```yaml
debt_id:
debtor:
creditor:
kind: gratitude | revenge | oath | life_debt | family | reputation
origin_event:
exact_obligation:
witnesses: []
public_knowledge:
status:
```

### Technique

```yaml
technique_id:
name:
lineage:
prerequisites: []
capabilities: []
costs: []
known_counters: []
current_possessor:
witnesses: []
demonstrated_in: []
```

Also track faction hierarchy and doctrine, alliances, injury and recovery limits, aliases and who knows them, weapon ownership history, succession claims, and rumors as `true`, `false`, or `unverified`.

## Failure Modes

- Treating wuxia as generic cultivation or unlimited magical scaling.
- Letting power tiers replace moral conflict.
- Using sects as interchangeable enemy teams.
- Ignoring how reputation changes access and obligation.
- Granting techniques without lineage, limitation, or consequence.
- Resolving revenge without defining the protagonist's justice code.
- Making every authority corrupt in the same way.
- Treating `xia` as identical to European chivalry.
- Forgetting injury, travel, witnesses, weapon custody, or oath wording.

## Research Basis

- Leon Hunt, [Wuxia Fictions: Chinese Martial Arts in Film, Literature and Beyond](https://www.brunel.ac.uk/creative-writing/research/entertext/documents/entertext061/ET61WuxIntroED.pdf).
- Haomin Gong et al., [Ironizing the martial protagonist: Jin Yong and the web novelists](https://www.nature.com/articles/s41599-024-04256-y).

Use these sources as genre context. The operational structures above are practical synthesis, not claims that every wuxia story must follow one formula.
