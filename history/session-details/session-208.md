---
session: 208
date: 2026-07-10
track: graph
model: Fable 5 (orchestrator) + Sonnet 4.6 (events triage ×4) + Haiku 4.5 (fresh-verify ×5)
graph_mutation: yes
---

# Session 208 — F&B review-bucket recovery (1,440 quarantined rows → 995 edges + 201 event nodes)

## The problem

The S200–S202 bulk apply quarantined 1,440 `reconcile-review.jsonl` rows — every candidate edge
touching a NAME the router couldn't confidently route was dropped. S203 wrote the class-table policy
(`REVIEW-BUCKET-TRIAGE-PLAN-s203.md`); this session executed it end-to-end. The extractor
(`recovery-s208/extract-quarantined.py`) sized the prize precisely: 1,361 edge-shaped rows + 278
event rows across 931 names in 39 units.

## The idempotency question (resolved by design, then proven)

The continue prompt's open mechanics question — "can a unit re-run without double-applying?" — turned
out to have a stronger answer than a dup-guard: **recovery mode never re-processes landed rows at
all.** The new `--recover` flag on `fab-reconcile-candidates.py` takes a per-unit
`{name: slug|"CREATE"}` map and processes ONLY rows touching mapped names. Since a quarantined name's
rows by definition never landed, double-apply is impossible by construction; mint's P4 same-quote
dedup is the second belt (it caught exactly 1 cross-unit repeat in the real run). Design guards:

- run_id gets a `-recovery` suffix so mint's substring re-run guard treats recovery as its own run;
- unmapped names can never CREATE (an original-apply CREATE may have been folded/renamed by
  adjudication surgery — re-minting would resurrect it); they land in the recovery out-dir's review
  file as `recovery-unmapped-create-skipped` (6 fired);
- an authoritative map override wins over resolve/blocklist/cluster/type-gate (the curator saw the
  disambiguator).

Proof on a scratch copy of edges.jsonl (checkpoint commit `382de1f201` first): (A) 6 edges land,
(B) identical re-run ABORTs on run_id, (C) new-run_id re-run skips all 6 as same-quote dups,
(D) zero dedup-key overlap between recovered candidates and the live graph.

## Name curation

- **Small classes (43):** hand-decided with graph lookups. Notable traps: `cheese` is the FOOD node
  (the assassin is `cheese-ratcatcher`); "Septon Murmison" auto-proposed to his own assassination
  EVENT (person node is `murmison`); `queen-rhaenys`/`princess-rhaenys` are ship artifacts; "Mouse"
  is Marilda of Hull's NICKNAME so the extracted `Marilda SAME_AS Mouse` would have landed a
  self-loop — dropped. `OrphanMaker` (junk-classed!) mapped to the real `orphan-maker` sword;
  "Sins of the Flesh"/"A Wanton's Tale" mapped to `a-caution-for-young-girls` as title-versions;
  "Six Times to Sea" CREATEd as object.text. needs-vocab 5 dropped (no vocabulary match; the regent
  row may return with the edge-vocab retrofit).
- **no-decisive-margin (172 rows / 51 names):** fully disambiguator-decided per unit, no LLM needed.
  The review quarantine earned its keep: the deterministic scorer would have picked WRONG on Laena
  Velaryon (daughter-of-alyn scored above the actual mother-of-Baela) and Queen Visenya
  (daughter-of-daemon over the Conquest queen). High Septon rows resolved per-era where the
  disambiguator pinned one (aegons-conquest/aenys-i/jaehaerys-i/dance/regency), 6 dropped as
  era-ambiguous. `prentys-tully` recovered all 4 "Lord Tully" rows. `ronnel-arryn` is a disambig hub
  with no node for the boy king — pre-minted `ronnel-arryn-son-of-sharra`.
- **unresolved-status (929):** head = 147 names ≥2× curated (70 auto via slugify-exact/fresh-resolve,
  77 hand-reviewed); **tail = 415 names / 406 proposal rows DROPPED wholesale** per the S203 policy,
  logged in `tail-drop-log.json`. Root cause note: `resolve()` returns status `candidates` even when
  candidate #1 is an exact slug match, so the router's clean-hit rule never fires for "Kingsguard",
  "Iron Throne", "King's Landing" — a resolver-rank fix would kill this whole class at the source but
  touches the S190-pinned golden cases; logged as its own potential track.

## Deferred-events vein (276 rows)

Token-screen vs the 1,032-slug event inventory (11 exact / 9 subset / 256 clear) → 4 parallel Sonnet
create-or-skip agents (they read candidate nodes; 215 CREATE / 54 MAP / 5 DROP / 2 COLLIDE) → an
orchestrator semantic-dup scan (token Jaccard ≥0.6) over the CREATEs caught what per-slice agents
can't see: 3 same-event pairs across units (Death of Septon Barth ×2, Death of Prince Aemon ×2,
Alyssa's flight = Escape of Alyssa; later-sorted unit flipped to MAP onto the earlier unit's pending
mint) and 5 different-event slug collisions needing disambiguated premints (two High-Septon deaths,
two Vulture-King deaths, birth-of-Viserys I vs II, the QWNW's death vs the Conqueror's sister's,
the 48 AC vs Dance yielding-of-the-red-keep, Maegor's trial-of-seven vs the concept node). Then
**192-CREATE Haiku fresh-verify: 190 CONFIRM / 2 REJECT-DUPE** (the-green-council →
green-council-conceals-death-of-viserys; aegons-first-coronation → aegons-coronations), folded back
by `apply-verify-verdicts.py`. The 11 creates from the 3 late-failing units (their maps referenced
pending mints, so phase-A reconcile aborted correctly) were covered by the Sonnet triage + token
screen + mint's fail-fast line-check; the batch-5 Haiku agent confused itself by matching each landed
node against its own file, so its output was discarded.

## Landing + gates

`run-recovery.py` drove reconcile→mint→merge per unit in sorted order (pending-mint MAPs resolve
because creator units mint first). 37/39 clean on the first pass; 2 mint manifest-guard aborts from
stale phase-A node files (the guard working as designed) — cleaned and re-run. **Totals: +995 edges
(52 disputed, all with in_universe_source), 201 created event nodes, prose merges on ~120 names.
edges.jsonl 25,313 → 26,308; event nodes 1,034 → 1,242.**

`fab-semantic-gate` initially FAILed victim_in_harm_gate on 6 edges — S207 fallout, not recovery
damage: S207's retype (battle→war, off-schema→incident) flipped those edges' TARGET subtypes out of
the harm set after the fact. P1 policy retype (VICTIM_IN→PARTICIPATES_IN, annotated) → **gate 4/4
PASS; pytest 1457; deno 100.** Index churn surgical per the S206 recipe: 8,416 timestamp-only files
reverted via a `git cat-file --batch` comparison ignoring `generated_at`, 5 meaningful modifications
+ all new-node index files kept.

## Decisions (Matt, live)

- **`event.betrothal` SANCTIONED** (architecture.md row + 3 S207-folded nodes retyped up + 5 new
  mints); **`event.betrayal` REJECTED** on the data (59 BETRAYS edges carry the relation; ~4-5 nodes
  would claim the leaf; marquee betrayals stay battle/conspiracy by narrative shape).
- Bonus: `mellos` added to the `in_universe_source` enum everywhere + the derive map; the one landed
  edge that lost the attribution (viserys-i KILLS lyonel-strong, the Harrenhal-fire rumor) repaired
  mushroom→mellos — the derive had picked the wrong chronicler from the passage neighborhood
  (Mushroom blames Corlys in the same paragraph; the king-did-it musing is Mellos's, verified
  verbatim at fab-heirs-of-the-dragon-15-p03:121).
- New standing mechanism: the reconciler CREATE path now schema-gates event subtypes
  (`normalize_event_subtype`, synced with `s207-event-retype.py` + architecture.md) so bulk creates
  can never reintroduce the S207 off-schema drift class.

## Residue

- **76 dispute-held recovery rows** (`out/*/dispute-review.jsonl`) — hedge-neighborhood quarantine;
  drain via fab-dispute-preclassify → adjudicate → fab-dispute-inject (one short sitting).
- 42 quote-quarantine rows (normal rate); 237 partner-endpoint drops (tail-drop cost, closed).
- Node-type promotion sweep rider not needed for the new creates (schema-gated at mint); the S207
  conservative-retype promotion sweep stays a todos MED item.
- Prod deploy of the enlarged bundle: Matt-gated as always (DEPLOY.md — manual netlify deploy).
