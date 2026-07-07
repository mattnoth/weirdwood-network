# Targaryen name-space overlap audit — F&B UPDATE-not-CREATE de-risking

**Purpose:** Guarantee the Fire & Blood enrichment pass reconciles onto existing nodes instead of minting Targaryen (and Dance-adjacent) duplicates. Read-only audit; nothing written to `graph/nodes/`.

**Scope:** 21 `*-targaryen` same-name clusters + Dance houses (Velaryon, Hightower, Strong, Baratheon, Celtigar, Rogare, Cole, Cargyll). Sources: `working/wiki/data/same-name-clusters.json`, `graph/nodes/**`, `graph/edges/edges.jsonl`, `working/wiki/data/page-categories.jsonl`, `sources/wiki/_raw/*.json`.

---

## Verdict

**The Targaryen name-space is SAFE for UPDATE-not-CREATE — the wiki layer already covers essentially all of it.** All 25 Dance principals and every prominent Conquest/Jaehaerys/Regency figure spot-checked has a node (with only two genuinely obscure exceptions). Across all 27 audited clusters there are **zero true duplicates** — every same-name pair is separated by distinct parents, regnal number, or birth/death years. Discriminators are dense: only **3 members carry a single discriminator** and all 3 are minor. **The real risk is not duplicate-CREATE — it is confident-wrong-MATCH onto disambiguation-page trap nodes** (already flagged as R1 in `fable-review.md`). This audit confirms the specified mitigation works: the blocklist join (`page-categories.jsonl` "Disambiguation pages" ∩ node `wiki_source`) cleanly catches **all 12 live Targ/Dance disambig trap nodes** with no false negatives, and adds one trap (`aerys-targaryen`) the same-name-cluster pack's `trap_nodes` field missed (harmless — no node file exists for it).

**Counts at a glance:** true duplicates **0** · under-discriminated members **3** · genuine coverage gaps **2 (both trivial)** · disambiguation trap nodes in namespace **12 live + 1 pageonly** · redirect trap nodes (handled by parallel step) **3**.

---

## 1. Suspected duplicates

**NONE.** Programmatic scan of all 27 clusters (81 members) for the "same person minted twice" signature (shared parent-set AND identical regnal) returned zero hits. Every same-name pair differs in at least one hard discriminator. Spot-checked the two theoretically-closest cases against wiki lead prose:

| Pair | Verdict | Evidence |
|------|---------|----------|
| `aegon-iii-targaryen` vs `viserys-ii-targaryen` (both children of Daemon+Rhaenyra, dates 120/122) | DISTINCT | Different born (120 vs 122) + different regnal (III vs II); brothers, `_raw/Aegon_III_Targaryen` |
| `rhaenys-targaryen` (Conquest, Aegon I's sister-wife) vs `rhaenys-targaryen-daughter-of-aemon` (the Queen Who Never Was) | DISTINCT | Different parents, born (—/10 vs 74/129), era; already correctly split |

No SAME_AS / merge actions required.

---

## 2. Under-discriminated members (reconciler would be forced to review or risk wrong-match)

Members carrying **only one** independent discriminator (parents / spouse / regnal / born-died / era / key_title). Everything else in the namespace has ≥2.

| Slug | Has | Missing | Note for reconciler |
|------|-----|---------|---------------------|
| `aegon-targaryen-young-griff` | key_title=prince | parents, dates, spouse, regnal, era | (f)Aegon / Young Griff — parentage is deliberately contested in-canon; expected to stay review-only. Not an F&B figure. |
| `maekar-targaryen` | spouse=dyanna-dayne | everything else | **Redirect page → Maekar I** (`_raw` = "Redirect to: Maekar I Targaryen"); NOT a real distinct member. Handled by the parallel redirect step; do not treat as a live match target. |
| `robert-baratheon` | parents (steffon+cassana) | everything else | **Redirect page → Robert I** (`_raw` = "Redirect to: Robert I Baratheon"). Same as above. Not F&B-relevant. |

**Practical takeaway:** the only under-discriminated members are either (a) `young-griff` (out of F&B scope, review-only by design) or (b) redirect artifacts the parallel step already removes. **No in-scope F&B Targaryen is dangerously under-discriminated** — the Dance/Conquest/Jaehaerys members all carry parents + dates (and usually era or regnal).

---

## 3. Coverage gaps (prominent F&B figures with NO node → legitimate future CREATE)

Checked all 25 Dance principals + ~50 further F&B figures (Conquest, Jaehaerys era, Dance secondaries, Regency, dragonseeds, dragons) against `graph/nodes/characters/`.

**All 25 Dance principals HAVE nodes:** rhaenyra-targaryen, daemon-targaryen, aemond-targaryen, helaena-targaryen, aegon-ii/iii-targaryen, viserys-i-targaryen, alicent-hightower, otto-hightower, criston-cole, corlys-velaryon, rhaenys-targaryen-daughter-of-aemon, baela-targaryen, rhaena-targaryen-daughter-of-daemon, jacaerys/lucerys/joffrey-velaryon, nettles, hugh-hammer, ulf-white, addam-velaryon, alyn-velaryon, larys/lyonel/harwin-strong.

**Dragons covered:** sunfyre, vhagar, caraxes, vermithor, meleys, seasmoke, balerion, quicksilver (all present as `character.dragon`).

**Apparent gaps that RESOLVE to existing nodes (NOT real gaps):**
- "Black Aly" → `alysanne-blackwood` (alias `"Black Aly Blackwood"` in frontmatter)
- Gwayne Hightower (Otto's son) → `gwayne-hightower`
- Quicksilver (dragon) → `quicksilver` (`character.dragon`)
- Orwyle → `orwyle`

**Genuine gaps (both trivial, low F&B salience):**

| Missing figure | Salience | Recommendation |
|----------------|----------|----------------|
| Sam Stark (Cregan-era Stark, one-line mention) | very minor | Legit CREATE if a unit rosters him; not a Dance principal |
| Rickon Stark son of Benjen "Antler" (obscure early Stark) | very minor | Same |

**Conclusion:** the graph already covers the entire F&B principal cast. The legitimate-CREATE surface is limited to a handful of trivially-minor named figures — exactly the "probably most already covered" state Matt expected. F&B should default hard to UPDATE.

---

## 4. Additional junk / trap nodes

Two distinct kinds of bare-name junk exist in the namespace. **The distinction is load-bearing for the blocklist design.**

### 4a. Disambiguation-page trap nodes (the R1 confident-wrong-match magnet)

Live node files whose `wiki_source` is a wiki **disambiguation page** ("X is the name of several members of House Targaryen…"). Each is a contentless boilerplate stub (`## Identity: X is a character from the AWOIAF wiki`) that the resolver returns as a **confident exact HIT** for a bare first-name query ("Aegon", "Prince Aemon") — the R1 corruption path.

**12 live disambig trap node files in namespace:** `aegon-targaryen`, `aemon-targaryen`, `baelon-targaryen`, `baelor-targaryen`, `daella-targaryen`, `daeron-targaryen`, `gaemon-targaryen`, `jaehaerys-targaryen`, `maegor-targaryen`, `rhaena-targaryen`, `vaella-targaryen`, `manfred-hightower`.

**Blocklist verification (the key result):** the mitigation specified in `fable-review.md` R1 — block nodes whose page is in the `page-categories.jsonl` "Disambiguation pages" category — **catches all 12 of these with zero misses** (verified join below). All are already listed in the same-name-cluster pack's `trap_nodes` field too, so cluster-aware routing is a second independent net.

- Graph-wide, the disambig-category ∩ node-`wiki_source` join yields **39 trap nodes** (13 in Targ/Dance namespace incl. the page-only `aerys-targaryen`; 26 elsewhere: `alysanne`, `royce`, `stranger`, `valyrian`, `willow`, `damon-lannister`, `leo-tyrell`, `lyonel-tyrell`, `walda-frey`, several `house-*` pages, etc.). The F&B blocklist should use this full graph-wide set, not just the Targaryen subset.

### 4b. Redirect-page nodes (parallel step's job — noted, not re-solved)

`_raw` body = "Redirect to: <Regnal> Targaryen/Baratheon". These are handled by the parallel deterministic redirect step. In namespace:

- `aenys-targaryen` → Aenys I · `maekar-targaryen` → Maekar I · `robert-baratheon` → Robert I

These are **NOT** in the "Disambiguation pages" category (verified: all three return `in-disambig-cat=False`), so the 4a blocklist alone will NOT catch them — they genuinely need the separate redirect map. Confirmed the parallel step's examples (`aenys-targaryen`, `maekar-targaryen`, `robert-baratheon`) match exactly.

### One thing the same-name-cluster pack's `trap_nodes` field missed

`aerys-targaryen` is a disambiguation page (in the category) but the `aerys targaryen` cluster's `trap_nodes` is `[]`. **Harmless** — there is no `aerys-targaryen.node.md` file and 0 edges, so nothing to match onto — but it confirms `trap_nodes` (built per-cluster) is a *weaker* signal than the disambig-category join. **Use the page-categories join as the primary blocklist; treat `trap_nodes` as secondary.**

### Not junk (verified, keep)

`martyn-hightower` opens with a hatnote ("For the son of Lord Ormund…, see…") but is a **real person page** (Lord Martyn, Beacon of the South, full infobox) — a legitimate node, the elder Martyn. Not a trap.

---

## The single most important thing the F&B track must handle

Run the disambiguation-trap **blocklist before any MATCH-first resolution**, sourced from the graph-wide `page-categories.jsonl` "Disambiguation pages" ∩ node-`wiki_source` join (39 nodes; 12 live in the Targaryen/Dance namespace). This is verified to catch every live Targaryen disambig trap. It must run **alongside** — not instead of — the parallel redirect-map step, because the 3 redirect traps (`aenys-`, `maekar-`, `robert-`) are NOT in the disambiguation category and the blocklist alone will miss them. With both nets in place, the namespace is safe: 0 duplicates, full principal coverage, all traps caught.
