# Historical-Anchor Notes: battle-of-the-camps

**Hub:** `battle-of-the-camps` (event.battle)
**Produced:** 2026-06-15
**Source chapters:** agot-catelyn-10 (ch. 64, Whispering Wood — pre-battle), agot-catelyn-11 (ch. 72 — Riverrun aftermath, primary source for this battle)

---

## Structural Attachments

- **LOCATED_AT → riverrun** — emitted (wiki-only tier-2). The battle was fought in Jaime's three siege camps encircling Riverrun.
- **PART_OF → war-of-the-five-kings** — SKIPPED (already exists; 1 outgoing edge confirmed via graph-query).

---

## Edge Summary

| Edge Type    | Count | Book-tier-1 | Wiki-tier-2 |
|--------------|-------|-------------|-------------|
| LOCATED_AT   | 1     | —           | 1           |
| COMMANDS_IN  | 3     | 2           | 1           |
| FIGHTS_IN    | 4     | 1           | 3           |
| ATTENDS      | 1     | 1           | —           |
| VICTIM_IN    | 2     | 1           | 1           |
| **Total**    | **11**| **5**       | **6**       |

---

## Participant Decisions

**robb-stark** — COMMANDS_IN (tier-1 book). Catelyn XI line 65: "It was Robb … and Brynden." Robb led two columns of armored horse against the middle camp. Node verified.

**brynden-tully** — COMMANDS_IN (tier-1 book). Same quote, Catelyn XI line 65. Blackfish led Robb's van, attacked the north camp. Node verified.

**tytos-blackwood** — FIGHTS_IN (tier-1 book). Catelyn XI line 19: "It had been Lord Tytos who led the sortie that plucked her brother from the Lannister camp." Direct on-page narration. Node verified.

**hoster-tully** — ATTENDS (tier-1 book). Catelyn XI line 63: Hoster tells Catelyn he had himself carried to the gatehouse battlements to watch the battle. Explicit non-combatant witness. Node verified.

**edmure-tully** — VICTIM_IN (tier-1 book). He was held prisoner in the Lannister camp from the earlier battle under the walls of Riverrun and was freed by Tytos's sortie during this battle. Not a combatant during the Battle of the Camps itself. Catelyn XI line 19 is the book anchor. Node verified.

**jon-umber** — FIGHTS_IN (tier-2 wiki). Wiki narrates Greatjon burning the siege towers. Note: catelyn-10 line 83 places the Greatjon blowing a horn in the Whispering Wood (the prior battle), not the Camps — that quote was NOT used. Wiki-only for this battle. Node verified.

**andros-brax** — VICTIM_IN (tier-2 wiki). Drowned attempting to cross on rafts from the middle camp. No book chapter narrates his death directly. Wiki body is sole source. Node verified.

**forley-prester** — FIGHTS_IN (tier-2 wiki). Led the southern-camp retreat. Wiki-only; not mentioned in catelyn-11. Node verified.

**grey-wind** — FIGHTS_IN (tier-2 wiki). Wiki: "allegedly kills four men and a dozen horses." The catelyn-10 passage with Grey Wind howling/tearing flesh is the Whispering Wood battle (ch. 64), not the Camps — NOT used as the evidence quote. Wiki-only for the Camps. Node verified (character.direwolf).

**jaime-lannister** — COMMANDS_IN (tier-2 wiki, with caveat). Jaime set up and commanded the three-camp siege that became the Battle of the Camps, but was already captured at Whispering Wood before the battle itself commenced. The wiki explicitly frames him as the camp commander ("the Lannister force is unaware of their commander's defeat"). COMMANDS_IN is assigned on the grounds that the battle is defined by the disposition of his force. Edge note records his absence from the battle itself. Node verified. Assigning COMMANDS_IN rather than FIGHTS_IN since he was not personally present during the fighting.

---

## Unresolved Participants

None. All 10 named participants resolved to existing nodes.

---

## Skipped / Deliberately Excluded

- **PART_OF → war-of-the-five-kings** — already exists (confirmed outgoing edge); not re-emitted per spec.
- **Tyroshi sellsword** (leads freeriders, switches sides) — unnamed character, no node; skipped per spec.
- **House Umber / House Mallister** (mentioned as contingents in wiki body) — no named individual beyond jon-umber; not emitting house-level role edges, only character nodes per this batch.
- **Marq Piper / Karyl Vance** (wiki: harassed Jaime during the siege) — these are participants in the siege harassment raids preceding the battle, not the Battle of the Camps itself; excluded.
- catelyn-10 Grey Wind and Greatjon quotes deliberately NOT used as evidence here — that chapter narrates the Whispering Wood battle (ch. 64), a distinct prior engagement.
