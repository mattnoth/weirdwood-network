# D&E Graph-Ingest Pressure Test — S222

Fresh, independent, adversarial review of `working/dunk-egg-graph-ingest/out/emit.jsonl` (255 edges)
and `out/alias-adds.jsonl` (69 aliases), per the pressure-test brief. Read-only against the repo;
this file is the only write.

## 1. Cite integrity — stratified sample (60 rows, 20/book)

Random seed 42, stratified by `evidence_book`. For each row, opened `evidence_ref` file at the cited
line ±3 and did a whitespace/quote-normalized substring check for `evidence_quote`.

**Result: 60/60 CONFIRM.** Every sampled quote is verifiably present at (or within 3 lines of) its
cited line. No fabricated or mis-cited quotes found in the sample. This part of the pipeline is solid.

## 2. Resolution correctness + 3. Type/direction — sample + targeted audit

Read all 60 sampled rows in context. **59/60 semantically CONFIRM** (right person, right edge
direction, quote actually supports the claim — including a couple that looked suspicious at first
glance and turned out correct on inspection, e.g. `gormon-peake KILLS lord-hayford` correctly
resolves "a lord with three castles on his shield" to Peake via his house sigil, matching Peake's own
wiki bio verbatim).

**1/60 REJECT: row 112** — `aegon-v-targaryen PARENT_OF brynden-rivers` (tmk:599). Quote: *"Born
bastard," Ser Uthor agreed mildly, "but his royal father made him legitimate as he lay dying."* The
extraction file itself correctly labels the source as **"King Aegon (IV)"** — Pass 1 got it right.
Bloodraven's own node states `PARENT_OF: Brynden Rivers ← Aegon IV Targaryen`. The ingest resolved to
Aegon **V** (Egg) instead — a different person three generations later.

That one miss led me to distrust the `resolved-context-present` / `resolved-context-prior` /
`resolved-firstname-unique` resolution paths (119 of 510 endpoint-resolutions, ~40% of rows touch at
least one) and audit them directly rather than trust the random sample alone. That audit surfaced a
**systematic** pattern, not an isolated typo — four distinct failure modes, all confirmed against the
source text and the target node files:

**a) Targaryen generational namesake collisions** (exactly the risk class named in the brief):
- `102` `daemon-i-blackfyre PARENT_OF aemon-targaryen-son-of-maekar-i` (tss:703) — the quote is about
  Daemon I Blackfyre's own son **Aemon Blackfyre**, killed as a child at Redgrass Field. Resolved
  instead to Maester Aemon (b.198–d.300 AC, dies decades later in ADWD). His node literally says "One
  of 3 Aemon Targaryens — see disambiguation."
- `105` `brynden-rivers KILLS aemon-targaryen-son-of-maekar-i` (tss:703) — same wrong Aemon.
- `112`, `141`, `142` — three separate `PARENT_OF` rows all attribute Aegon IV's bastards
  (Bloodraven, Bittersteel, Daemon I Blackfyre) to **Aegon V** instead. The source text is explicit
  ("King Aegon the Unworthy," "King Aegon (IV)" in the extraction table) — this is a pure resolver
  defect, not a Pass-1 problem.
- `231` `daemon-ii-blackfyre SIBLING_OF aegon-v-targaryen` (tmk:1571) — quote is about Daemon II's
  actual older brothers **Aegon and Aemon Blackfyre** ("Wretched witless bullies... they took
  pleasure in tormenting me and Daemon"). Resolved the Aegon half to Egg. (The needs-map.csv
  correctly failed to resolve "Aegon, son of Daemon Blackfyre" 3 other times — this 4th mention
  slipped through to the wrong node instead of also failing.)
- `251`, `253` — `brynden-rivers SIBLING_OF/ADVISES aerys-ii-targaryen` (tmk:2063, tmk:1987). The
  extraction table says "Aerys I" explicitly, other rows in the *same* part-file correctly resolve
  "Aerys I" → `aerys-i-targaryen` (rows 66, 67, 107, 185) — these two specifically drifted to Aerys
  **II** (the Mad King, ~50 years later, unborn at the time of TMK).

**b) Cross-house/era namesake collision — Alyn Cockshaw vs. Alyn Velaryon.** The extraction file
(`tmk-dunk-01-p07`) names this character **"Lord Alyn Cockshaw"** in every single relationship row,
consistently. Six emit rows resolved him to `alyn-velaryon` (Alyn Oakenfist, an unrelated Velaryon
admiral from a different century) instead of `alyn-cockshaw` — while one sibling row (`201`,
`alyn-cockshaw SEEKS daemon-ii-blackfyre`) correctly resolved to the right node from the same file.
Wrong-node rows: `176` OPPOSES, `208` DEFEATS (as victim), `225` ATTACKS, `228` CONSPIRES_WITH, `233`
LOVER_OF, `236` CONTRACTED_WITH. This misattributes an entire antagonist subplot (attempted murder of
Dunk, jealous obsession with Daemon II, the well fight) onto the wrong person.

**c) Curated-map anchor error, not just an algorithm bug.** `working/dunk-egg-graph-ingest/curated-map.csv`
lines 57–61 hand-anchor "Ser Damon Lannister" / "the Grey Lion" / "Lord Lannister" → `damon-lannister`.
That node is a **disambiguation-hub stub** (`disambiguation_hub: true`) whose one listed member,
`damon-lannister-son-of-jason`, is born in **244 AC** — decades after D&E and definitely not the
Redgrass Field-era Lord of Casterly Rock Arlan unhorsed 16 years before THK. There is currently no
correct node in the graph for the D&E-era "Grey Lion." Affects `20` (`arlan-of-pennytree DEFEATS
damon-lannister`) and `192` (`quentyn-ball DEFEATS damon-lannister`), plus 4 alias-adds (see §4).
This matters because it shows even the hand-curated "safe" bucket (242/510 endpoint resolutions) isn't
fully clean — I only spot-checked a couple of curated-map anchors and found this.

**d) Type-incoherent fuzzy matches** (raw name → wrong node *type*, found while auditing the
`resolved-firstname-unique` bucket):
- `74` `rohanne-webber KILLS her-little-flower` (tss:297) — raw target was explicitly **"Her three
  husbands (unnamed)"** per the extraction table; resolved to an unrelated in-world song/text node
  (`type: object.text`).
- `76` `rowans-forced-confession SPOUSE_OF wendell-webber` (tss:303) — raw source was **"Lord Rowan's
  sister"** (unnamed); resolved to an unrelated `event.trial` node.
- `98` `daemon-i-blackfyre KILLS wild-hares` (tss:703) — raw target was **"Wild Wyl Waynwood"**, a
  named knight; resolved to an unrelated `organization.faction` node ("wild-hares"), apparently via
  a loose match on the word "Wild."

None of these should have resolved at all — they're exactly the shape of thing `quarantine.jsonl`'s
`unresolved-target`/`unresolved-source` reasons exist for, but the resolver accepted a wrong-typed
match instead of quarantining.

## 4. Alias review — all 69 rows

**59 APPROVE.** Spot-verified against the D&E text and grepped graph-wide for alias collisions;
flagging notable good catches: `Ser Theomore Bulwer`/`Old Ox` → `buford-bulwer` looks like a mismatch
at first glance (different first name) but it's a genuine in-text authorial inconsistency (thk/tmk
calls him both "Buford Bulwer" and "Ser Theomore of House Bulwer, the Old Ox") — correctly captured,
not a bug. `Ser Jay of House Caswell` → `joffrey-caswell` confirmed via the herald's actual line at
tmk:977. `gray pup` → `cerrick` confirmed (peasant slang for a young maester, tss:157).

**10 REJECT:**
| slug | alias | reason |
|---|---|---|
| `arlan-of-pennytree` | "The old man" | In-corpus collision: same phrase used in this text for Maester Cerrick (tmk:1023) and Ser Uthor Underleaf (tmk:1279), not just Arlan. Too generic to be a safe resolution anchor. |
| `arlan-of-pennytree` | "old man" | same |
| `damon-lannister` | "Ser Damon Lannister" | Target node is a disambiguation-hub stub for a different, much-later Damon Lannister (b. 244 AC) — see §3c. Wrong node, not just a risky one. |
| `damon-lannister` | "the Grey Lion" | same |
| `damon-lannister` | "Grey Lion" | same |
| `damon-lannister` | "Lord Lannister" | same, and independently over-generic |
| `aegon-v-targaryen` | "Aegon" | Bare "Aegon" is already an alias on `aegon-targaryen-son-of-rhaegar.node.md` — direct graph-wide collision. Also proven dangerous by §3a (this exact batch mis-resolved bare "Aegon" three separate times). |
| `aegon-v-targaryen` | "Aegon Targaryen" | Already an alias on **two** other nodes (`aegon-targaryen.node.md`, `pisswater-prince.node.md`) — collision. |
| `daemon-ii-blackfyre` | "the Pretender" | `daemon-i-blackfyre` already carries "Daemon the Pretender" as an established alias — bare "the Pretender"/"Pretender" would be ambiguous between father and son (both led Blackfyre rebellions). |
| `daemon-ii-blackfyre` | "Pretender" | same |

**Minor (not rejected, flagged for hygiene):**
- `wet-wat` | "The younger Wat brother" / "younger Wat brother" — not wrong, but these are descriptive
  clauses explaining the nickname's origin, not phrases anyone actually calls him by. Low value as a
  lookup alias; recommend dropping, not blocking.
- 6 proposed aliases are **already present** on the target node's frontmatter and would be no-op/
  duplicate adds if applied blindly: `lyonel-baratheon`/"The Laughing Storm", `baelor-targaryen-son-of-daeron-ii`/"Baelor Breakspear",
  `valarr-targaryen`/"The Young Prince", `brynden-rivers`/"Lord Rivers", `brynden-rivers`/"Lord Bloodraven",
  `brynden-rivers`/"Bloodraven". Contract in `README.md` says alias-adds should only be surface forms
  *missing* from the node — this violates that contract. Low severity (idempotent if the apply script
  dedupes), but worth fixing in the script.

## 5. Systematic sweep (whole file)

- Self-edges: **0**
- `SAME_AS`/`ALIAS_OF` leaked into emit.jsonl: **0**
- edge_type not UPPER_CASE: **0**
- Slugs (all 255 edges + 69 aliases, 116 distinct) with no node file under `graph/nodes/`: **0** — all
  resolve to *some* node, which is precisely the problem: several resolve to the *wrong* node (§3) or
  to a node of the wrong type (§3d) rather than failing to resolve at all.
- Duplicate (source, type, target) triples in emit.jsonl: **0**

## Final tallies

- Cite-integrity sample: 60/60 CONFIRM
- Resolution/semantics sample + targeted audit: 41 CONFIRM, 0 AMBIGUOUS, **19 REJECT** (1 from the
  random sample, 18 found via targeted audit of the risky resolution-status buckets — see full list
  below)
- Aliases: 59 APPROVE, **10 REJECT**, 2 minor/non-blocking flags, 6 already-present duplicates

## FINAL VERDICT: PASS-WITH-EDITS

The cite-integrity layer and the curated-map/exact-match resolution paths are solid (100% and ~98%
clean respectively in sampling). But the `resolved-context-present` / `resolved-context-prior` /
`resolved-firstname-unique` resolution paths — **101 of 255 rows touch at least one** — have a
demonstrated high error rate (roughly 20–30% wrong among the subset I actually checked) concentrated
in genealogy-critical edges (`PARENT_OF`, `SIBLING_OF`) and one full antagonist subplot (Alyn
Cockshaw). This is systematic, not isolated noise — four distinct failure modes, not one. My audit of
that risky bucket was **not exhaustive** (~40 of 101 rows individually verified); do not bulk-apply
the remainder without a dedicated re-pass.

**Apply now:**
- All 255 emit rows **except** the 19 listed below.
- All 69 aliases **except** the 10 listed below (and consider dropping the 2 `wet-wat` ones for
  quality).

**Do not apply without further review:**
- The ~61 remaining rows in the `resolved-context-present`/`resolved-context-prior`/
  `resolved-firstname-unique` buckets that I did not individually check (safe to identify
  mechanically: any row where either `source_resolution_status` or `target_resolution_status` is one
  of those three values, minus the 19 already confirmed-bad above).
- Fix `curated-map.csv` lines 57–61 (`damon-lannister` anchors) before any re-run — either mint a
  proper node for the D&E-era "Grey Lion, Lord of Casterly Rock" or map those raw names to `SKIP`.

**Drop — 19 confirmed-wrong emit rows** (0-indexed position in `emit.jsonl`):

```
20  arlan-of-pennytree DEFEATS damon-lannister                     — wrong/stub node (§3c)
74  rohanne-webber KILLS her-little-flower                         — wrong-typed node (§3d)
76  rowans-forced-confession SPOUSE_OF wendell-webber               — wrong-typed node (§3d)
98  daemon-i-blackfyre KILLS wild-hares                             — wrong-typed node (§3d)
102 daemon-i-blackfyre PARENT_OF aemon-targaryen-son-of-maekar-i    — wrong Aemon (§3a)
105 brynden-rivers KILLS aemon-targaryen-son-of-maekar-i            — wrong Aemon (§3a)
112 aegon-v-targaryen PARENT_OF brynden-rivers                      — wrong Aegon gen. (§3a)
141 aegon-v-targaryen PARENT_OF aegor-rivers                        — wrong Aegon gen. (§3a)
142 aegon-v-targaryen PARENT_OF daemon-i-blackfyre                  — wrong Aegon gen. (§3a)
176 alyn-velaryon OPPOSES duncan-the-tall                           — wrong Alyn (§3b)
192 quentyn-ball DEFEATS damon-lannister                            — wrong/stub node (§3c)
208 glendon-flowers DEFEATS alyn-velaryon                           — wrong Alyn (§3b)
225 alyn-velaryon ATTACKS duncan-the-tall                           — wrong Alyn (§3b)
228 alyn-velaryon CONSPIRES_WITH daemon-ii-blackfyre                — wrong Alyn (§3b)
231 daemon-ii-blackfyre SIBLING_OF aegon-v-targaryen                — wrong Aegon (Blackfyre) (§3a)
233 alyn-velaryon LOVER_OF daemon-ii-blackfyre                      — wrong Alyn (§3b)
236 alyn-velaryon CONTRACTED_WITH uthor-underleaf                   — wrong Alyn (§3b)
251 brynden-rivers SIBLING_OF aerys-ii-targaryen                    — wrong Aerys gen. (§3a)
253 brynden-rivers ADVISES aerys-ii-targaryen                       — wrong Aerys gen. (§3a)
```

**Reject — 10 alias-adds** (slug, alias):

```
arlan-of-pennytree     "The old man"
arlan-of-pennytree     "old man"
damon-lannister        "Ser Damon Lannister"
damon-lannister        "the Grey Lion"
damon-lannister        "Grey Lion"
damon-lannister        "Lord Lannister"
aegon-v-targaryen      "Aegon"
aegon-v-targaryen      "Aegon Targaryen"
daemon-ii-blackfyre    "the Pretender"
daemon-ii-blackfyre    "Pretender"
```
