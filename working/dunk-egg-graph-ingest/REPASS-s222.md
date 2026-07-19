# S222 — Fresh Exhaustive Re-pass: D&E emit.jsonl Weak-Rung Endpoints

**Scope:** `working/dunk-egg-graph-ingest/out/emit.jsonl` (253 rows). Extracted every row where `source_resolution_status` OR `target_resolution_status` is `resolved-context-present`, `resolved-context-prior`, or `resolved-firstname-unique` — **101 rows**, matching the count stated in the task brief. Every one of the 202 endpoint slugs across those 101 rows resolves to *some* node file on disk (no orphans) — the errors found are all wrong-node, not missing-node.

## Counts

| Verdict | Count |
|---|---|
| CONFIRM | 76 |
| FIX | 21 |
| REJECT | 4 |
| **Total** | **101** |

That's a **25/101 (~25%) wrong-node rate** on the weak rungs — consistent with the prior pressure-test's 20–30% estimate, and confirming the demand for this exhaustive re-pass was justified.

## Method

For each row: pulled the raw quote + evidence_ref, opened both endpoint node files' frontmatter (name/type/aliases/era hints), and where ambiguous, read the source chapter text around the cited line for full context. Cross-checked node `type:` against expected `character.human` (four rows resolved to non-person types). Ran an automated slug→node index build first to confirm zero orphan targets, then did full manual verification of all 101 rows (not sampling) given the stakes.

## REJECT rows (4) — no safe fix available

1. **row 14** (`rohanne-webber KILLS her-little-flower`) — target is a *song* (`type: object.text`, "Her Little Flower," sung by Dareon in AFFC), completely unrelated to the quote. The quote's actual victims ("three of her husbands") are unnamed in text — unresolvable.
2. **row 15** (`rowans-forced-confession SPOUSE_OF wendell-webber`) — source is an unrelated Fire & Blood-era `event.trial` node. The real subject, "Lord Rowan's sister," is unnamed in the D&E text — unresolvable.
3. **row 46** (`sefton-staunton SERVES high-septon`) — target is the generic `type: title` node, not a person. The text never names a specific High Septon contemporaneous with TSS (~211 AC) — unresolvable to a person node.
4. **row 62** (`kyle-the-cat SWORN_TO joffrey-caswell`) — quote explicitly says Kyle's sword "was sworn to **his father**," not to Joffrey Caswell himself. Joffrey's father is unnamed in text — unresolvable.

## FIX rows (21) — right node exists, unambiguous swap

**Targaryen generational collisions (mode a) — 8 rows**, all confirmed present as warned:
- **rows 28, 47, 48** — `aegon-v-targaryen` used as father of the Great Bastards (Bloodraven/Bittersteel/Daemon Blackfyre); text explicitly says "King Aegon the Unworthy" / "his royal father" — that's **Aegon IV**, not Aegon V (Egg). This is the *exact* pattern the task brief said was "already rejected" once — it reappeared 3 more times in this batch. → `aegon-iv-targaryen`
- **rows 22, 23** — "Young Aemon" who died at Redgrass Field carrying Blackfyre is Daemon I's own twin son, not Aemon Targaryen (Maester Aemon, son of Maekar I). Same already-known pattern, 2 more instances. → `aemon-blackfyre`
- **row 87** — Cockshaw's childhood-bullies "Aegon and Aemon" are the Blackfyre twins (Daemon I's sons who died at Redgrass Field), not Aegon V Targaryen (Egg). A new variant of the same collision family — Aegon-the-Targaryen vs. Aegon-the-Blackfyre. → `aegon-blackfyre`
- **row 99** — Bloodraven's king (whom he serves as Hand) is Aerys I (TMK's reign, ~211 AC), not Aerys II (the Mad King, ~60+ years later). → `aerys-i-targaryen`
- **row 98** — compound error: resolved to Aerys II (wrong era) *and* wrong person — the quote's "my half brother" refers to Bittersteel (Aegor Rivers), not any Aerys. → `aegor-rivers`

**Cross-person/cross-house first-name collisions (mode b) — 6 rows**, a new specific instance beyond the Alyn-Cockshaw case already known:
- **rows 60, 72, 83, 86, 88, 90** — `alyn-velaryon` (Alyn Oakenfist, a Dance-of-the-Dragons-era Velaryon admiral) substituted for **Alyn Cockshaw**, the TMK antagonist. Confirmed by full-text grep: every "Alyn"/"Lord Alyn" mention in `tmk-dunk-01.md` is Cockshaw — there is no Velaryon in this chapter at all. This is the exact "already rejected" pattern from the prior pass, but it's baked into **6 separate edges** in this batch (both as source and target), meaning the underlying resolver/curated-map entry for "Alyn" is still wrong, not just one bad row. → `alyn-cockshaw`
- **rows 29, 30** — `simon-leygood` (a living suitor courting Rohanne, per rows 43/44) substituted for **Simon Staunton**, Sefton's dead brother / Rohanne's 3rd husband. Both share only the first name "Simon." → `simon-staunton`
- **rows 31, 32** — `rolland-storm` (Bastard of Nightsong, unrelated character) substituted for **Rolland Uffering**, named explicitly in the quote as Rohanne's 4th husband. → `rolland-uffering`

**Wrong-type/generic-stub matches (mode c) — 2 rows**, plus a new sub-pattern:
- **row 20** — target resolved to `wild-hares` (an `organization.faction` node) via a stray match on "Wild"; the quote names "Wild Wyl Waynwood," which has its own person node with alias "Wild Wyl." → `wyl-waynwood`
- **row 13** — target resolved to a **disambiguation-hub stub** (`alysanne`, `disambiguation_hub: true`, whose one listed candidate is a wrong-era Alysanne daughter of Aegon IV) instead of the specific `alysanne-osgrey` node that exists and matches the quote (Eustace Osgrey's daughter). This is a **new failure sub-mode**: the resolver landing on a disambiguation-hub placeholder node even when an exact, correctly-surnamed node is available in the graph. → `alysanne-osgrey`
- **row 45** — target resolved to a generic `bracken` stub instead of the specific `lord-bracken-father-of-otho` node, which exists and matches the quote exactly (Otho's dying father on the Trident). Same stub-vs-specific sub-pattern as row 13. → `lord-bracken-father-of-otho`

## New failure mode beyond the four known ones

**Stub/disambiguation-hub matches when a specific node exists** (rows 13, 45): the resolver is landing on generic placeholder nodes (`disambiguation_hub: true`, or bare-surname stubs like `bracken`) rather than the specific, correctly-disambiguated node that's already present in the graph under an unambiguous slug (`alysanne-osgrey`, `lord-bracken-father-of-otho`). This isn't a namesake-era or cross-house collision — the *right* node exists and is well-formed; the resolver just didn't prefer it over a weaker generic stub. Worth a resolver-priority fix (prefer specific over generic/hub nodes) independent of the four known modes.

No direction/semantic (mode d) violations were found in this batch — all KILLS/DEFEATS/ATTACKS agent-victim pairings that resolved to real people were pointed the right way.

## Systemic observation

Two of the "already rejected" known-bad patterns from the prior pressure-test (Alyn Cockshaw→alyn-velaryon; Aegon IV→aegon-v-targaryen as father of the Great Bastards; Aemon Blackfyre→aemon-targaryen-son-of-maekar-i) are **still live in the resolver/curated-map layer** — they didn't recur as isolated one-offs, they recurred at every single occurrence of the ambiguous name in this batch (6/6 Alyn rows, 3/3 Aegon-IV-as-father rows, 2/2 Aemon-Blackfyre rows). That strongly suggests the underlying curated disambiguation map (not just individual pass-1 rows) still has the wrong slug cached for these three names, and will keep producing the same error on any future D&E batch until the map entry itself is corrected — not just these 21 rows patched.

## Files

- `working/dunk-egg-graph-ingest/repass-selected-s222.jsonl` — the 101 extracted rows (raw, unmodified)
- `working/dunk-egg-graph-ingest/repass-enriched-s222.jsonl` — same 101 rows + resolved node name/type for both endpoints
- `working/dunk-egg-graph-ingest/repass-verdicts-s222.jsonl` — one verdict object per row (this deliverable)
