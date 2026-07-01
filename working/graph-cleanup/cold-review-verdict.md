# Cold-Review Verdict — parent-conflation re-plan (PARENT_OF cleanup)

Reviewer: fresh cold reviewer. Read-only. No graph mutation, no git add.
Scope: independently re-derived counts + verified the S179 classifier's three-class
proposal (`working/graph-cleanup/parent-edge-proposal.jsonl`) against LOCAL wiki cache
`sources/wiki/_raw/` and `web/data/nodes.json` quote counts.

## Bottom line

**The re-plan does NOT hold as-is. Do not auto-apply the DUPLICATE_PARENT_NODE merges.**
The REDUNDANT class is provably safe and can auto-apply. But the DUPLICATE class contains
at least one **destructive false merge** (the "two Aerions"), several **house-node-as-parent
mis-bins**, and the canonical-selection rule (highest quote-count wins) is **unsafe for the
bare-slug-vs-variant shape** — it can keep a wrong-era namesake and delete the correct node.
The GENUINE class is also under-counted: five of its eight nodes are conflation buckets
(multiple real people under one bare slug), not "one person + extra edges." And the classifier
misses a 4th failure mode: exact-duplicate PARENT_OF edges.

## 1. Independent recount + 88-vs-89 resolution

- PARENT_OF edges total: **1688**.
- Nodes with **>2 distinct parents (set)**: **88**.
- Nodes with **>2 PARENT_OF edges (list)**: **89**.
- Edges into the >2 set: **344 distinct** (347 rows in the proposal file — see below).

**Resolution:** The classifier counts *edges* per child (`list`), not *distinct parents*
(`set`). The one extra node is `tyrion-lannister`, which has 3 PARENT_OF edges but only 2
distinct parents because **`tywin-lannister → tyrion-lannister` appears TWICE** (an exact-
duplicate edge). So 89 = the classifier's edge-count number; 88 = the true biological-anomaly
count. The doc's "88" and the script's "89" are both defensible; they measure different things.
The 344 vs 347: three children have an exact-dup PARENT_OF edge — `tyrion-lannister`
(tywin×2), `oppo` (hop-bean×2), `penny` (hop-bean×2) — inflating the row count by 3.

## 2. REDUNDANT_CHILD_STUB (124 edges) — VERDICT: SAFE, auto-apply OK

I checked **all 124** (not just a sample): for every REDUNDANT edge P→C, a disambiguated
variant `C-...` exists **and already carries P**. Zero false REDUNDANTs. No REDUNDANT child
is itself a variant. The delete-only claim is sound; deleting these edges cannot lose a fact
because the good node demonstrably holds it.

Caveat (not a blocker): 9 bare children lose *all* parents after REDUNDANT deletion
(`aemon-targaryen`, `daeron-targaryen`, `rhaena-targaryen`, `aegon-frey`, `daella-targaryen`,
`gaemon-targaryen`, `leo-tyrell`, `luthor-tyrell`, `robert-frey`). This is correct — those bare
slugs are ambiguous conflation buckets whose real parentage lives on the variants — but it means
those bare nodes become parent-less orphans that likely want a later redirect/cleanup (out of
scope here).

## 3. DUPLICATE_PARENT_NODE (61 edges) — VERDICT: DO NOT AUTO-APPLY

The 61 rows split into two shapes:

- **45 "prefix" merges** (bare slug ↔ `-son-of-X` / `-daughter-of-X` variant). SAME structural
  pattern as REDUNDANT, but here the *parent* is the double-noded one. Safe ONLY when the bare
  and the variant are the same person AND the merge keeps the variant.
- **16 "name" merges** (maiden/married like Elenda Caron=Elenda Baratheon, or bare-house-token
  like `sunderly`/`bracken`/`mormont`/`piper`).

Confirmed-CORRECT merges (wiki-verified):
- **Elenda Caron = Elenda Baratheon** — `sources/wiki/_raw/Elenda_Caron.json` is a literal
  redirect: *"Redirect to: Elenda Baratheon."* Borros Baratheon's issue = Cassandra, Maris,
  Ellyn, Floris, Royce Baratheon (all the flagged children). TRUE merge. ✅
- **Damion Lannister's father** — `Damon_Lannister_(son_of_Jason)`: *"Issue Damion Lannister."*
  Bare `damon-lannister` is a disambig page ("name of multiple members"); the variant is the
  right father. Merge keeps the variant. ✅ (direction happens to be safe)
- **Edric Stark (son of Cregan)** for `argelle-stark` — Argelle's wiki Father link points to
  `/Edric_Stark_(son_of_Cregan)`. Bare `edric-stark` is a *different* Lord of Winterfell
  (wiki disambig header confirms two Edrics). Merge keeps the `-son-of-cregan` variant. ✅

**FALSE MERGE — HIGH RISK (blocker):** the "two Aerions."
- `sources/wiki/_raw/Aerion_Targaryen.json` header: *"For the Lord of Dragonstone and father of
  Aegon the Conqueror, see Aerion Targaryen (son of Daemion)."* These are **two different people
  ~200 years apart.**
- The bare `aerion-targaryen` is **Aerion the Monstrous** (son of Maekar), **qc = 8** — a real,
  prominent D&E character (his node quotes: *"Come out, come out, little knight, it's time you
  faced the dragon"*). `aerion-targaryen-son-of-daemion` (the correct Conqueror-era father) is
  **qc = 0**.
- For `aegon-i-targaryen`, `rhaenys-targaryen`, `visenya-targaryen`, the classifier's
  highest-qc-wins rule picks the **bare (Monstrous, qc8)** as canonical and proposes **merging
  the correct Lord-of-Dragonstone node INTO Aerion the Monstrous.** Executing this would (a) wire
  Aerion the Monstrous as father of Aegon the Conqueror, and (b) destroy the real Lord of
  Dragonstone node. This is exactly backwards.
- **Correct fix:** these three are GENUINE_EXTRA_PARENT, not merges. DELETE the
  `aerion-targaryen (Monstrous)` edge into Aegon-I/Rhaenys/Visenya; KEEP
  `aerion-targaryen-son-of-daemion`. No node merge.

**Mis-bin — house node treated as a person (4 Greyjoy + Bracken/Mormont/Piper rows):**
`sources/wiki/_raw/Sunderly.json` = *"Redirect to: House Sunderly."* The bare `sunderly` is a
**house node, not a person.** Same for `bracken` (→ lady-bracken), `mormont`, `piper`. The
proposed action "merge parent node X → person" is wrong (you'd merge a House into a person).
The correct action is: DELETE the spurious house-as-parent edge (or reassign to the person node
`lady-sunderly-wife-of-quellon-greyjoy` etc.). Outcome-equivalent on the edge, but the "merge
nodes" instruction must not be executed literally.

**General rule the classifier violates:** `same_person()` matches on shared first-name token /
slug prefix, which is unsafe for ASOIAF's dense namesake reuse (Aerion, Edric, Brandon, Rickon,
Aegon, Rhaenys all recur across eras). It happens to be right in most prefix cases only because
the variant usually out-quotes the bare node and wins canonical — but the Aerion case proves the
rule can invert into destruction. **Every DUPLICATE merge needs a per-pair same-person
confirmation before applying; do not auto-apply on the qc heuristic.**

## 4. GENUINE_EXTRA_PARENT (8 nodes) — partially mislabeled; really 2 sub-kinds

| node | graph parents | correct ≤2 (wiki) | verdict |
|---|---|---|---|
| joffrey-baratheon | cersei, robert, jaime | cersei + jaime (bio); robert = presumed/legal | **KEEP all 3** — legit special case, tag robert as presumed-father, NOT an error to prune |
| rickard-stark | edwyle-stark, jon-stark, marna-locke | edwyle + marna-locke (wiki: Father Edwyle, Mother Marna Locke) | prune **jon-stark** (ancient KitN, wrong) |
| sansa-stark | eddard, catelyn, jeyne-manderly, rickon-stark-son-of-cregan | eddard + catelyn (wiki) | prune **jeyne-manderly** + **rickon-stark-son-of-cregan** (different-era Sansa namesake conflation) |
| brandon-stark | 13 parents | rickard + lyarra (this is Ned's brother) | **CONFLATION BUCKET** — bare slug holds ≥6 different Brandon Starks; needs node-split, not edge-prune |
| rickon-stark | 6 parents | eddard + catelyn (Ned's son) | **CONFLATION BUCKET** — also holds Rickon son of Cregan etc. |
| rhaella-targaryen | 4 parents | jaehaerys-ii + shaera (Aerys II's queen) | **CONFLATION BUCKET** — also an earlier Rhaella; aegon-son-of-aenys + rhaena-daughter-of-aenys are the other Rhaella's parents |
| elaena-targaryen | 4 parents | aegon-iii + daenaera (the famous Elaena) | **CONFLATION BUCKET** — daenys + gaemon-son-of-aenar belong to a pre-Conquest Elaena |
| rhaenys-targaryen | 7 parents | (multiple Rhaenyses) | **CONFLATION BUCKET** — Conqueror's sister (aerion-son-of-daemion + valaena) vs Aemon's daughter (aemon-son-of-jaehaerys + jocelyn) vs Rhaegar's daughter (rhaegar + elia); the bare `aerion-targaryen` edge here is again the wrong-Aerion error |

So GENUINE splits into: **3 true per-edge fixes** (rickard, sansa, + joffrey=keep-as-is) and
**5 conflation buckets** that need node-splitting (a different remedy than the class implies).

## 5. What the classifier MISSED / MIS-BINNED (4th & 5th failure modes)

1. **Exact-duplicate PARENT_OF edges (4th mode, MISSED).** `tyrion-lannister←tywin` ×2,
   `oppo←hop-bean` ×2, `penny←hop-bean` ×2. The classifier clustered tyrion's two tywin edges
   and emitted **two identical `tywin KEEP` rows** — silently preserving the dup instead of
   flagging one for deletion. A trivial dedup pass on (source,target,edge_type) should run first;
   it also reconciles the 344-vs-347 / 88-vs-89 gap.
2. **Namesake conflation buckets (5th mode, MIS-BINNED into GENUINE).** Bare slugs
   (`brandon-stark`, `rickon-stark`, `rhaella-targaryen`, `elaena-targaryen`, `rhaenys-targaryen`,
   `sansa-stark` partly) accumulate parents from *multiple distinct people*. The remedy is
   node-splitting/disambiguation, not "review-and-prune one extra edge."
3. **Unsafe canonical rule.** highest-qc-wins picks the wrong node whenever a bare high-qc
   namesake collides with a correct low-qc variant (the Aerion failure). Canonical selection
   should prefer the **disambiguated variant slug** over a bare slug regardless of qc, and must
   never merge across a wiki disambiguation boundary.
4. **`parent_node_missing` is 0 everywhere** — good, no dangling-parent edges in this set.

## Misclassification table (evidence-backed)

| child | proposal says | should be | evidence |
|---|---|---|---|
| aegon-i-targaryen / rhaenys-targaryen / visenya-targaryen | MERGE `aerion-targaryen-son-of-daemion`→`aerion-targaryen`; KEEP bare | DELETE bare `aerion-targaryen` edge; KEEP `-son-of-daemion` | Aerion_Targaryen.json header: "…father of Aegon the Conqueror, see Aerion Targaryen (son of Daemion)"; bare node qc=8 = Aerion the Monstrous |
| aeron/balon/euron/urrigon/victarion-greyjoy | MERGE node `sunderly`→lady-sunderly | DELETE/REASSIGN house-as-parent edge (`sunderly` is a house) | Sunderly.json: "Redirect to: House Sunderly" |
| alysanne/bess/catelyn-bracken | MERGE `bracken`→lady-bracken | same house-node caveat | `bracken` bare = house token |
| tyrion-lannister | 2× `tywin KEEP` | delete 1 duplicate PARENT_OF edge | two identical rows in edges.jsonl |
| brandon/rickon/rhaella/elaena/rhaenys-targaryen buckets | GENUINE_EXTRA_PARENT (per-edge review) | NODE SPLIT (conflation bucket) | multiple wiki disambig pages per bare slug |
| joffrey-baratheon | GENUINE_EXTRA_PARENT | KEEP all 3 (robert = presumed father, by design) | canon: Robert presumed, Jaime biological |

## Recommended revision before any mutation

1. **Dedup PARENT_OF edges first** (drop exact (src,tgt,type) repeats). Re-run the audit.
2. **Auto-apply REDUNDANT_CHILD_STUB deletes** — verified safe (124/124).
3. **Do NOT auto-apply DUPLICATE merges.** Change canonical rule to prefer the disambiguated
   variant slug; refuse any merge that crosses a wiki disambiguation/redirect boundary; route the
   Aerion trio and all bare-house-token pairs to per-pair review. Elenda/Damion/Edric-style pairs
   are fine after that guard.
4. **Re-bin GENUINE:** keep joffrey as-is (presumed-father special case), do the 2 true prunes
   (rickard←jon-stark, sansa←jeyne-manderly+rickon-son-of-cregan), and route the 5 conflation
   buckets to a node-split track, not edge-prune.
