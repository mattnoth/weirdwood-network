# Historical-Anchor Notes: siege-of-riverrun

**Hub:** `siege-of-riverrun` (event.battle; AFFC Jaime POV)
**Produced:** 2026-06-15

## Structural edges

- **LOCATED_AT → riverrun** — emitted (node confirmed via graph-query)
- **PART_OF → war-of-the-five-kings** — SKIPPED (already exists per `--neighbors` check: 1 outgoing edge to `war-of-the-five-kings`)

## Participant role edges (10 total)

| Edge type | Source slug | Evidence | Chapter |
|-----------|-------------|----------|---------|
| COMMANDS_IN | daven-lannister | book-pass1 tier-1 | affc-jaime-02 |
| COMMANDS_IN | jaime-lannister | book-pass1 tier-1 | affc-jaime-06 |
| COMMANDS_IN | ryman-frey | book-pass1 tier-1 | affc-jaime-05 |
| COMMANDS_IN | brynden-tully | book-pass1 tier-1 | affc-jaime-05 |
| VICTIM_IN | edmure-tully | book-pass1 tier-1 | affc-jaime-05 |
| ATTENDS | emmon-frey | book-pass1 tier-1 | affc-jaime-06 |
| ATTENDS | edwyn-frey | book-pass1 tier-1 | affc-jaime-06 |
| ATTENDS | desmond-grell | book-pass1 tier-1 | affc-jaime-07 |
| ATTENDS | robin-ryger | book-pass1 tier-1 | affc-jaime-07 |
| ATTENDS | jeyne-westerling | book-pass1 tier-1 | affc-jaime-07 |

**Total:** 11 edges (1 LOCATED_AT + 4 COMMANDS_IN + 1 VICTIM_IN + 5 ATTENDS)

## Evidence split

- **Book-grounded (tier-1):** 11 / 11 — every edge sourced to a verbatim AFFC Jaime chapter quote
- **Wiki-only (tier-2):** 0

## Role assignment notes

- **Daven Lannister** — COMMANDS_IN: explicitly described as holding command at the siege ("Ser Daven has command there") before Jaime's arrival
- **Jaime Lannister** — COMMANDS_IN: arrived to take overall strategic command, negotiated surrender directly with Edmure and the Blackfish; the entire AFFC Jaime arc (chapters 05–07) centers on his directing the siege's conclusion
- **Ryman Frey** — COMMANDS_IN: led 2,000 Freys, directed the gallows-coercion strategy, personally commanded Frey forces north of the Tumblestone; demoted/expelled by Jaime mid-siege
- **Brynden Tully** — COMMANDS_IN: commanded Riverrun's defense throughout; prepared stores, expelled mouths, directed archers from walls; defender side
- **Edmure Tully** — VICTIM_IN: held hostage under gallows with noose, coerced into surrendering the castle; captured, not a voluntary combatant
- **Emmon Frey** — ATTENDS: present in siege camp as designated new Lord of Riverrun, participated in war council, but not a field commander or combatant
- **Edwyn Frey** — ATTENDS: attended war council representing Frey interests, eventually inherited Ryman's command after Ryman was expelled; on-page at siege
- **Desmond Grell** — ATTENDS: Riverrun master-at-arms, part of the garrison; chose the black at surrender rather than leave
- **Robin Ryger** — ATTENDS: Riverrun captain of guards, part of the garrison; chose the black at surrender
- **Jeyne Westerling** — ATTENDS: was inside Riverrun during the siege (held by Brynden Tully as leverage); released when castle surrendered

## Unresolved / skipped participants

None among the named targets. All 10 participant nodes resolved successfully.

**Skipped (unnamed / no slug):**
- Ser Ilyn Payne — present at siege (accompanies Jaime), but role is as Jaime's bodyguard/executioner, not a siege participant per se; no node check attempted as not in task list
- Walder Rivers — present at war council (affc-jaime-06:131); not in task list, no node check performed
- Lady Genna Lannister — present at siege camp and war council; not in task list, no node check performed
- Addam Marbrand, Strongboar, Forley Prester — present at war council; not in task list, not checked
