# Review-bucket triage plan — 1,440 reconcile-review rows (S203)

Deterministic grouping of every `reconcile-review.jsonl` row across the 35 applied units
(+ 4 S200 smoke units). Per design §10.10: summary-level policy, NOT row-by-row reads.
Each row is a NAME the reconciler could not confidently route to a slug — every candidate
edge touching that name was quarantined (never landed). Recovery = resolve the name, re-run
the affected units' injection for just those rows.

## Class table (by `reason`)

| Class | Rows | What it is | Recommended policy | Est. effort |
|---|---|---|---|---|
| `unresolved-status:candidates` | 929 | Name got only weak fuzzy candidates. Top offenders are famous fixtures: Kingsguard (25), Iron Throne (11), King's Landing (10), Septon Eustace (12), Septon Barth (10), Iron Bank (10), Citadel (8), Seven Kingdoms (8), Night's Watch (8)… | **KEEP head / DROP tail.** A curated name→slug map of the repeat names recovers the bulk: 72 map entries cover 364 rows (≥3×); 147 entries cover 514 (≥2×). Long-tail one-offs (~415): DROP — passing mentions, poor cost/benefit. | Map is semi-deterministic (each row already carries its candidate list; human confirms). One sitting + a re-inject script run. |
| `event-dedup-risk:candidates` | 221 | Event names deferred because fuzzy matched SOME existing event — but the matches are noise ("Death of Queen Helaena" → hizdahr-orders-drogon-killed). 211 distinct names; visibly includes real missing majors (Death of Queen Helaena, births of Dance principals, Battle of the Stepstones, Betrothal of Aegon III and Daenaera…). | **KEEP — this is the second deferred-events vein.** Re-screen with the S203 token-screen (exact-token match vs event-slug inventory), auto-clear no-real-dupe rows, then the same create-or-skip triage run as the 37-row sidecar batch. Some will match nodes minted S201–S203. | Own session, same machinery as S203 deferred-events triage. |
| `no-decisive-margin` | 172 | Two+ same-named slugs, router couldn't pick (Corlys vs corlys-son-of-daemon; Rhaena ×17; High Septon ×17; Balerion ×14). Only 51 distinct names, and every row carries a `disambiguator` string ("the Sea Snake; Lord of the Tides…"). | **KEEP.** Disambiguator-aware micro-pass: deterministic keyword rules first (disambiguator tokens vs candidate node bodies), Haiku for residue. These are high-value majors. | Cheap; mostly deterministic. |
| `composite-name` | 57 | Compound event phrases ("Wedding of Viserys and Alicent", "Deaths of Runciter and Harrold Westerling"). NOT junk — several are missing events. | **KEEP — fold into the event-dedup-risk re-screen** (same create-or-skip pass). | Rides the same session. |
| `junk-character-candidate` | 18 | Router's junk screen flagged the name. | **DROP** (screen exists for a reason; spot-check 3 rows before deleting). | Minutes. |
| `type-mismatch` | 16 | Correct entity, wrong node category ("Sea Snake"→corlys-velaryon, "Massey"→house-massey). The matches are actually right. | **KEEP — hand-map all 16** (they're aliases the resolver should learn; add `aliases:` entries where natural-phrase). | Minutes. |
| `house-surname-existing-node` | 13 | Plural surname ("Mootons"→house-mooton). Routing is correct. | **KEEP — auto-accept rule** (plural-surname → house node). | Deterministic one-liner. |
| `bare-first-name-miss` | 6 | Bare first name, no candidate. | Hand-triage. | Minutes. |
| `needs-vocab` | 5 | Edge type not in locked vocabulary. | Hand-triage (likely DROP or re-type). | Minutes. |
| `blocklisted-no-cluster-entry` | 2 | — | Hand-triage. | Minutes. |
| `in_universe_source-not-in-enum` | 1 | `mellos` not in chronicler enum. | Add `mellos` (Grand Maester Mellos IS a F&B chronicler source) or map to closest; re-inject the one row. | Trivial. |

## Recommended sequencing

1. **Small classes first** (16+13+6+5+2+1 = 43 rows): one sitting, mostly deterministic. Do in a residue step.
2. **`no-decisive-margin` (172)**: deterministic disambiguator rules + Haiku residue. Own step, cheap.
3. **`unresolved-status` head-map (≥2× names, 147 entries → 514 rows)**: one curated-map sitting + re-inject. DROP the ~415-row tail explicitly (log the drop).
4. **`event-dedup-risk` + `composite-name` (278 rows)**: the second deferred-events vein — own session, reuse the S203 token-screen + fresh-verify + mint rhythm.

## Open mechanics question (for the recovery session, not now)

The quarantined edges themselves are NOT persisted separately — recovery requires re-running
`fab-reconcile-candidates.py` (or a targeted re-inject) per affected unit with a name→slug
override map. Verify the reconciler accepts an override input before building the map; if
not, that's a small script-builder job.
