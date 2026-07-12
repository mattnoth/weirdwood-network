# Roles slice S212 — orchestrator adjudication record

**Input:** 244 candidates (4 Sonnet proposers over top-50 ranked zero-role events; chunks 79/61/56/48).
**Fresh-verify (Haiku, adversarial):** 233 CONFIRM / 5 AMBIGUOUS / 6 PROBLEM.
**Outcome:** 236 accepted → mint · 8 dropped · 5 wiki_only + 2 no_node parked (`parked.json`).

## Drops (8)

| id | edge | reason |
|---|---|---|
| R2-04 | brynden-tully PARTICIPATES_IN battle-of-the-fords | not at the event — remote strategic advisor on the western campaign; Edmure commanded the Fords |
| R2-07 | harry-strickland PARTICIPATES_IN taking-of-storms-end | council dissent ≠ participation; consistent with existing S147 `OPPOSES golden-company-sails-for-westeros` |
| R2-42 | cleon VICTIM_IN siege-of-astapor | corpse-victim (already dead when cut down) — not a harm-patient; `siege` also not a harm subtype; beat stays node prose |
| R3-09 | thaddeus-rowan PARTICIPATES_IN lysene-spring | torture under coercion is passive suffering, not active involvement; `incident` harm-gate blocks VICTIM_IN — no honest role slot |
| R3-29 | lyanna-stark VICTIM_IN abduction-of-lyanna | **harm-gate violation the verifier missed** — node typed `event.incident` (fails gate); orchestrator ALSO holds the drop on honesty grounds: `incident` typing reads as deliberate neutrality on abduction-vs-elopement and VICTIM_IN would assert the contested reading. Rhaegar `AGENT_IN` tier-2 stands (agent under either reading). Node deliberately NOT retyped. |
| R4-04 | karyl-vance PARTICIPATES_IN siege-of-raventree | advises Jaime at Riverrun; not shown at the siege |
| R4-05 | daven-lannister PARTICIPATES_IN siege-of-raventree | proposed equipment transfer (overruled); not shown at the siege |
| R4-10 | denys-mallister PARTICIPATES_IN fight-at-the-bridge-of-skulls | quote shows a raven FROM him reporting the fight, not participation |

## The 5 AMBIGUOUS dispositions (3 adjusted, 1 kept as-proposed, 1 dropped — R2-42 above)

- **R1-04** renly COMMANDS_IN war-of-the-five-kings — verifier note (proclamation-not-command-action) accepted; **quote upgraded** to Renly's own "with my own host around me" (acok-catelyn-02:237). Tier-1 stands (bedrock canon).
- **R1-22** robert-i COMMANDS_IN roberts-rebellion — same class; **quote upgraded** to "Lords great and small had flocked to Robert's banners" (agot-eddard-02:139). Tier-1 stands.
- **R4-48** polliver FIGHTS_IN capture-of-harrenhal — kept, **downgraded tier-1 → tier-2** (presence explicit, combat borderline).
- R4-18 edric-dayne FIGHTS_IN battle-at-the-burning-septry — kept as proposed (already tier-2 for the "Ned" disambiguation).

## History checks (S159/S211 records, per the S211 lesson)

- 13 of 50 target events appear in prior fresh-verify/adjudication records — all prior rulings were **causal-edge class** (ENABLES/PRECEDES/FORESHADOWS), none role-edge; no adjudicated drop re-proposed.
- **lysene-spring**: S211 rejected Unwin-Peake near-dups (canonical hub = the-treason-trials). No chunk-3 candidate touches unwin-peake — clean.
- Exact-dup check vs live edges.jsonl: **0 dups** among the 236.

## Parked (not minted)

- 5 wiki_only rows (3 Reyne-Tarbeck roles: roger-reyne / walderan-tarbeck / stafford-lannister; 2 war-across-the-water COMMANDS_IN: mathos-ii-arryn / house-stark) — S211 precedent: wiki-only facts park, they don't mint through the book-quote gate.
- 2 no_node rows (the tattooed criminal executed as Davos; one chunk-2 row).

## Residue flags for todos/worklog

1. **reyne-tarbeck-revolt canon conflict**: book (asos-jaime-06:91) attributes the Tarbeck imprisonment to **Tytos**; the node's wiki-sourced Origins prose says Tywin. Stale-prose fix candidate.
2. **Tommard Heddle killing** (Whitewalls, Duncan the Tall single combat) is a genuine harm beat with no event node — future sub-event mint candidate (S212 routed him FIGHTS_IN second-blackfyre-rebellion per the war-node harm-gate).
3. Three top-50 events honestly yielded 0 roles: war-for-the-dawn (pure prophecy discourse), dany-lost-on-dothraki-sea, robb-receives-false-news-of-brans-death (both `incident`-gated with no fitting role). Working as intended.
4. Chunk-1 flag confirms the Sansa/arrest-of-eddard-stark WITNESS_IN trap was correctly avoided (she hears through a door, never sees).
