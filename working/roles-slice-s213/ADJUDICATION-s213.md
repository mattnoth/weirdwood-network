# S213 roles round 2 — adjudication record

Input: 103 candidates (4 Sonnet proposer chunks over 24 events, frozen ranks 51–74
by score after the early-stop cut) + 4 Haiku fresh-verify verdict files.
Verdict totals: 94 CONFIRM / 5 AMBIGUOUS / 4 PROBLEM (one "PROBLEM" was the chunk-3
verifier logging a skipped wiki_only row, R3-19 — reconciles the 17-vs-18 count).

## Standing deterministic audits (all run pre-adjudication)

1. **Harm-gate (VICTIM_IN target subtype ∈ HARM_EVENT_SUBTYPES):** 18/18 OK — every
   kept VICTIM_IN targets an `event.battle` node. 0 failures.
2. **Prior-adjudication re-proposal grep (S211/S212):** no (source,target) pair
   co-appears in a prior adjudication file. Round-2 events are frozen ranks 51+, so
   round-1 territory (incl. all parked wiki_only rows) was excluded at selection.
3. **Duplicates vs edges.jsonl:** 0. **In-batch duplicates:** 0.
4. **Quote line-check (assemble-final.py):** 101/101 exact single-line substrings.

## Decisions on the 9 non-CONFIRM rows

| id | verdict | decision |
|----|---------|----------|
| R2-03 jaime PARTICIPATES_IN tommen-wedding | AMBIGUOUS quote-gap | **KEEP, quote swapped** to the on-page tasking line ("Cersei beckoned to Jaime. 'Lord Commander, escort His Grace…'") which Jaime accepts ("As you command") — the original quote showed only Cersei's order. |
| R2-04 cersei PARTICIPATES_IN tommen-wedding | AMBIGUOUS weak-quote | **RECLASSIFY → ATTENDS, quote swapped.** Same chapter says *Lady Alerie had made all the arrangements* — organizer-Cersei was overstated. Presence at the feast is on-page (watching the dancing). |
| R2-12 rodrik-cassel PARTICIPATES_IN fighting-in-the-hornwood | AMBIGUOUS not-shown-in-event | **DROP.** Quote places him "off east" mediating the dispute, geographically absent from the fighting. Adjacent administration, not the event. |
| R3-04 pate-of-longleaf COMMANDS_IN butchers-ball | PROBLEM quote-not-found | **KEEP — verifier FALSE POSITIVE.** Deterministic byte-check: the quote IS an exact single-line substring (the file itself mixes straight `I'll` and curly `o’` on one line; the verifier assumed uniform curly). |
| R3-08 stannis AGENT_IN stannis-retreats-to-dragonstone | PROBLEM unproven-act | **KEEP, tier-1 → tier-2.** The retreat is off-page; Salladhor Saan's report confirms it secondhand. Event node IS the retreat; agent identity isn't in doubt. |
| R3-10 roger-hogg COMMANDS_IN fighting-at-sows-horn | AMBIGUOUS commands-vs-fights | **KEEP as COMMANDS_IN.** Garrison commander whose men repel the raid; "we saw them off" is the commander reporting his garrison's action. Most-specific-role tiebreak favors command. |
| R3-11 rickard-karstark COMMANDS_IN fighting-at-sows-horn | AMBIGUOUS indirect-command | **DROP.** Bounty is an indirect incentive, not command of this skirmish; Rickard is dead (executed ASOS) before the AFFC raid. Causal/motivational, out of the roles slice's scope. |
| R3-16 hugh-hammer AGENT_IN the-sowing | PROBLEM quote-not-found | **KEEP — verifier FALSE POSITIVE.** Same as R3-04: byte-check passes; the quote's curly apostrophes match the file exactly. |
| R4-02 maegor COMMANDS_IN aegon-the-uncrowneds-rebellion | PROBLEM should-be-fights-in | **RECLASSIFY → FIGHTS_IN.** Quote shows personal arrival + dragon combat via Balerion; Davos Darklyn holds loyalist field command. Consistent with the umbrella-war sparing-FIGHTS_IN rule. |

Net: **101 kept** (30 COMMANDS_IN / 28 AGENT_IN / 18 VICTIM_IN / 8 PARTICIPATES_IN /
7 ATTENDS / 6 FIGHTS_IN / 2 HONORED_AT / 1 OFFICIATES / 1 WITNESS_IN), 2 dropped,
6 wiki_only + 0 no_node parked in `parked.json` (S211 precedent: wiki-only facts park,
they don't mint).

## Verifier-quality note (for the next round's design)

The Haiku verifier produced 2 false-positive `quote-not-found` PROBLEMs by assuming
uniform apostrophe encoding instead of byte-grepping (the fab OCR mixes straight and
curly within single lines). The deterministic line-check in assemble-final.py is the
authoritative quote gate — verifier quote verdicts are advisory; support/role verdicts
remain the verifier's real value (R4-02, R2-12 were genuine catches).

## Residue (recorded, NOT round-2 work)

- **Junk event nodes surfaced by the ranking:** `marriage` (typed event.battle,
  degree 0 — a generic wiki page minted as an event), `great-council`,
  `tourney-at-ashford-meadow` (both generic/degree ≤ 1). Below the cut; flag for a
  node-hygiene sweep.
- **Moat Cailin flaying massacre** (Ramsay flays 63 surrendered ironborn): the single
  most load-bearing harm beat of the siege went unminted — no per-victim nodes, and
  sieges carry no garrison-victim convention. Sub-event mint candidate (same class as
  S212's Tommard Heddle residue).
- **Lady Alerie Hightower** "made all the arrangements" for Tommen's wedding —
  clean PARTICIPATES_IN candidate discovered at adjudication; not minted this round
  (would bypass fresh-verify). Queue for a future dip.
- **seizure-of-westerlands-gold-mines**: chunk-3 flag suggests a likely chronology-edge
  bug on the node (see proposals-chunk3.json flags).
- **Harvest**: 4 harvest-chunk files with ~20 pointers, merge at endsession per the
  queue rule.
