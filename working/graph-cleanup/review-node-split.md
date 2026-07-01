# Review: Conflation-Bucket Node Split (Session 180, graph-parentage-cleanup track, phase 2)

Read-only judgement pass on 8 bare-slug nodes with >2 wired PARENT_OF parents. Sources: `sources/wiki/_raw/*.json` infoboxes, `graph/edges/edges.jsonl` (run_id `infobox-merge-20260613`), `graph/nodes/characters/*.node.md`, `web/data/nodes.json` quote counts.

No graph files modified — this is a proposal for a future edit pass.

---

## 1. `brandon-stark` (qc=7)

**Verdict:** primary = Brandon Stark "the wild wolf," Ned's older brother (born 262 AC, killed at the Great Hall, King's Landing, 282 AC — Aerys II's hostage-murder). Confirmed via `Brandon_Stark.json` infobox: `Father: Rickard Stark | Mother: Lyarra Stark`.

**KEEP:** `rickard-stark` (father), `lyarra-stark` (mother).

**DELETE:**
- `brandon-stark-shipwright → brandon-stark` (PARENT_OF). Evidence: `Brandon_Stark_(Shipwright).json` is an ancient King in the North ("the Shipwright"); his infobox `Issue` field says only "Brandon Stark" (unqualified), which the wiki-ingest pipeline generically resolved to the bare `brandon-stark` slug instead of the correct disambiguated son "Brandon the Burner." No `brandon-the-burner` / `brandon-stark-burner` node currently exists in `graph/nodes/characters/` to reassign to (checked directory listing — only `-shipwright` variant exists, not `-burner`). **DELETE, no reassignment target.**
- `edrick-stark → brandon-stark` (PARENT_OF). Evidence: `Edrick_Stark.json` is another ancient King in the North ("Snowbeard"); infobox `Issue` field literally reads "Grandfather of Brandon Stark" (not even a direct-child relationship) and again generically resolved to bare `brandon-stark`. Wrong edge_type semantics (grandparent mis-typed as parent) AND wrong person. **DELETE, no reassignment target.**

---

## 2. `elaena-targaryen` (qc=2)

**Verdict:** primary = Elaena Targaryen "the Dragon princess," daughter of Aegon III (born 150 AC). Confirmed via `Elaena_Targaryen.json` infobox: `Father: Aegon III Targaryen | Mother: Daenaera Velaryon`.

**KEEP:** `aegon-iii-targaryen` (father), `daenaera-velaryon` (mother).

**REASSIGN:**
- `gaemon-targaryen-son-of-aenar → elaena-targaryen` (PARENT_OF). Evidence: this is the father of the *other* Elaena — `Elaena_Targaryen_(daughter_of_Gaemon).json` (Century of Blood era, born 114–80 BC, Father: Gaemon Targaryen, Mother: Daenys Targaryen). **Confirmed**: `graph/nodes/characters/elaena-targaryen-daughter-of-gaemon.node.md` already exists. **REASSIGN** the edge there.

---

## 3. `joffrey-baratheon` (qc=22) — SPECIAL CASE, NOT RE-LITIGATED

**Verdict: KEEP ALL 3 PARENTS.** Cersei Lannister (biological mother), Jaime Lannister (biological father, incest), Robert Baratheon (presumed/legal father per Westerosi society + canon narrative framing). All three edges are simultaneously correct — not a conflation bug.

**Recommendation:** optionally annotate the `robert-baratheon → joffrey-baratheon` edge with a qualifier/note "presumed/legal father (not biological)" for downstream query clarity. Do not delete or merge anything.

---

## 4. `rhaella-targaryen` (qc=5)

**Verdict:** primary = Rhaella Targaryen, Aerys II's queen, mother of Rhaegar/Viserys/Daenerys (born 245–247 AC). Confirmed via `Rhaella_Targaryen.json` infobox: `Father: Jaehaerys II Targaryen | Mother: Shaera Targaryen`.

**KEEP:** `jaehaerys-ii-targaryen` (father), `shaera-targaryen` (mother).

**REASSIGN:**
- `aegon-targaryen-son-of-aenys-i → rhaella-targaryen` (PARENT_OF)
- `rhaena-targaryen-daughter-of-aenys-i → rhaella-targaryen` (PARENT_OF)

Both belong to an older/different Rhaella (per `Rhaella_Targaryen_(daughter_of_Aegon).json` — a septa born 42 AC, daughter of an Aegon and involved in the Aenys I generation). **Confirmed**: `graph/nodes/characters/rhaella-targaryen-daughter-of-aegon.node.md` already exists. **REASSIGN** both edges there.

---

## 5. `rhaenys-targaryen` (qc=4)

**Verdict:** primary = Rhaenys Targaryen, Aegon I's wife/sister, Conquest-era queen and dragonrider of Meraxes (died 10 AC at Hellholt). Confirmed via `Rhaenys_Targaryen.json` infobox (`Father: Aerion Targaryen | Mother: Valaena Velaryon`) AND the node file `graph/nodes/characters/rhaenys-targaryen.node.md` prose, which is entirely about the Conquest-era queen (Meraxes, Field of Fire, Dorne, rule of six, etc.) — matches qc=4.

**KEEP:** `aerion-targaryen-son-of-daemion` (father — this is the correctly-qualified slug), `valaena-velaryon` (mother).

**DELETE:**
- `aerion-targaryen → rhaenys-targaryen` (PARENT_OF, unqualified bare slug). Evidence: bare `Aerion_Targaryen.json` = "Aerion the Monstrous," Maekar I's son (Dunk & Egg era) — a completely different, much-later Aerion. This is a duplicate/miswired edge (the correctly-qualified `aerion-targaryen-son-of-daemion` sibling edge already covers the true father) — this bare-slug edge is redundant AND wrong-person. **DELETE.**
- `aemon-targaryen-son-of-jaehaerys-i → rhaenys-targaryen` (PARENT_OF). Evidence: this is the father of a *different* Rhaenys — `Rhaenys_Targaryen_(daughter_of_Aemon).json` ("the Queen Who Never Was," born 74 AC, daughter of Aemon Targaryen son of Jaehaerys I and Jocelyn Baratheon). A disambiguated node **already exists**: `graph/nodes/characters/` — confirmed via `edges.jsonl` line 18460/18461, which correctly wires `aemon-targaryen-son-of-jaehaerys-i` and `jocelyn-baratheon` to target_slug `rhaenys-targaryen-daughter-of-aemon`. The bare-slug edge to `rhaenys-targaryen` is a duplicate stray — since the correct edge already exists on the variant node, **DELETE** (not reassign — reassigning would create a duplicate on the variant, which already has it).

---

## 6. `rickard-stark` (qc=3)

**Verdict:** primary = Rickard Stark, Lord of Winterfell, Ned's father (born 230–250 AC, executed 282 AC by Aerys II). Confirmed via `Rickard_Stark.json` infobox: `Father: Edwyle Stark | Mother: Marna Locke`. Matches the note in the task prompt.

**KEEP:** `edwyle-stark` (father), `marna-locke` (mother).

**DELETE:**
- `jon-stark → rickard-stark` (PARENT_OF). Evidence: `jon-stark` is an ancient/different-era King in the North namesake (multiple Jon Starks exist in wiki disambiguation; none is Rickard's father — Rickard's father is unambiguously Edwyle per the infobox). No qualifier suggests which specific ancient Jon Stark this mis-wire came from; **DELETE, no reassignment target** identified in this pass.

---

## 7. `rickon-stark` (qc=7)

**Verdict:** primary = Rickon Stark, Eddard & Catelyn's youngest son (born 295 AC, POV-adjacent main-series character). Confirmed via `Rickon_Stark.json` infobox: `Father: Eddard Stark | Mother: Catelyn Tully`.

**KEEP:** `eddard-stark` (father), `catelyn-stark` (mother — Catelyn Tully wired as `catelyn-stark` node).

**DELETE/REASSIGN:**
- `benjen-stark-lord → rickon-stark` (PARENT_OF). Evidence: `Benjen_Stark_(lord).json` = an ancient Lord of Winterfell, Warden of the North, born before 84 AC — a different-era Benjen entirely unrelated to Ned's brother `benjen-stark`. His infobox `Issue` field resolved to the bare `rickon-stark` slug instead of the correctly-disambiguated variant node. **A variant node already exists: `graph/nodes/characters/rickon-stark-son-of-benjen.node.md`**, and edges.jsonl line 18573 shows the *correct* pipeline output was `benjen-stark → rickon-stark-son-of-benjen` (using the ancient Benjen's own bare-ish slug oddly, needs cross-check) — regardless, the stray edge on the bare `rickon-stark` (main-series Rickon) is a duplicate/mis-target. **REASSIGN this edge to `rickon-stark-son-of-benjen`** (the variant node already exists and is the correct target — this mirrors the sibling WRONG_NAMESAKE review's expected finding).

---

## 8. `sansa-stark` (qc=25)

**Verdict:** primary = Sansa Stark, Eddard & Catelyn's daughter, POV character (born ~286 AC per main series). Confirmed via `Sansa_Stark.json` infobox hatnote explicitly disambiguating "For the historical figure, see Sansa Stark (daughter of Rickon)" — i.e. the wiki itself treats bare `Sansa_Stark` as the main-series character by default.

**KEEP:** `eddard-stark` (father), `catelyn-stark` (mother).

**DELETE/REASSIGN:**
- `rickon-stark-son-of-cregan → sansa-stark` (PARENT_OF). Evidence: `Rickon_Stark_(son_of_Cregan).json` infobox lists `Issue: Sansa Stark` (unqualified) — this is the ancient historical Sansa (daughter of Rickon, born ~140s AC per `Sansa_Stark_(daughter_of_Rickon).json`, described on a shared fan-art caption "Two Sansa Starks: the daughter of Rickon... and daughter of Eddard"). **A variant node already exists: `graph/nodes/characters/sansa-stark-daughter-of-rickon.node.md`.** **REASSIGN this edge to `sansa-stark-daughter-of-rickon`** rather than deleting — the parent-fact (Rickon → historical Sansa) is real and belongs on the correct node.

---

## Summary table

| Node | Keep parent 1 | Keep parent 2 | Delete (no target) | Reassign (variant exists) |
|---|---|---|---|---|
| brandon-stark | rickard-stark | lyarra-stark | brandon-stark-shipwright, edrick-stark | — |
| elaena-targaryen | aegon-iii-targaryen | daenaera-velaryon | — | gaemon-targaryen-son-of-aenar → elaena-targaryen-daughter-of-gaemon (confirmed exists) |
| joffrey-baratheon | cersei-lannister | jaime-lannister | — (KEEP robert-baratheon too, tag as presumed/legal) | n/a |
| rhaella-targaryen | jaehaerys-ii-targaryen | shaera-targaryen | — | aegon-targaryen-son-of-aenys-i, rhaena-targaryen-daughter-of-aenys-i → rhaella-targaryen-daughter-of-aegon (confirmed exists) |
| rhaenys-targaryen | aerion-targaryen-son-of-daemion | valaena-velaryon | aerion-targaryen (bare, dup/wrong), aemon-targaryen-son-of-jaehaerys-i (dup of already-correct variant edge) | — |
| rickard-stark | edwyle-stark | marna-locke | jon-stark | — |
| rickon-stark | eddard-stark | catelyn-stark | — | benjen-stark-lord → rickon-stark-son-of-benjen (node exists) |
| sansa-stark | eddard-stark | catelyn-stark | — | rickon-stark-son-of-cregan → sansa-stark-daughter-of-rickon (node exists) |

## NEEDS-MATT: new-node creation flags

Two edges (`brandon-stark`'s `brandon-stark-shipwright` and `edrick-stark` parents) point at real, distinct ancient descendants ("Brandon the Burner" and an unnamed grandson) for whom **no disambiguated node currently exists**. These are plain deletes for now (no data is lost from the graph's canonical-character layer — the parent nodes `brandon-stark-shipwright` and `edrick-stark` still exist and still carry their own correct wiki facts; only the incorrect PARENT_OF cross-link to the wrong Brandon is removed). If Matt wants full genealogical completeness for the ancient Stark king-list line, a `brandon-stark-burner` node could be minted later and the `brandon-stark-shipwright → brandon-stark-burner` edge added — **this is a NEEDS-MATT call**, distinct from today's edge cleanup, since new-node creation is a bigger decision than deleting a stray edge.

The `elaena-targaryen` and `rhaella-targaryen` REASSIGN targets (`elaena-targaryen-daughter-of-gaemon.node.md`, `rhaella-targaryen-daughter-of-aegon.node.md`) were confirmed to already exist in `graph/nodes/characters/` — no new-node creation needed for those two. Same for `rickon-stark-son-of-benjen.node.md` and `sansa-stark-daughter-of-rickon.node.md`. Only the `brandon-stark` bucket's two extra parents (`brandon-stark-shipwright`, `edrick-stark`) lack any existing target node for their true child — those remain the only NEEDS-MATT new-node question in this batch.
