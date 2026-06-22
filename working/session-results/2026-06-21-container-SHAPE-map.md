# Container SHAPE map — synthesis of the 4-lens fan-out (S122)

> **What this is.** The 4 read-only lens subagents (A set+scope · B Jon/Bran · C seams · D retro-group)
> ran against the briefing + pressure-tested the S121 orchestrator PROPOSAL. This folds their reports into
> ONE shape map organized around the four expensive axes: **partition / boundaries / seams+ownership /
> granularity**. Names are provisional and reversible (a `containers:` tag is metadata, retag = find-replace
> via `stamp_containers.py`, touches no edges/walk/derived). **SHAPE is the costly axis** — this doc settles
> shape and surfaces the SET decision to Matt. Matt picks the SET; the orchestrator did NOT.
>
> Lens reports: `…-lensA-set-scope.md` · `…-lensB-jon-bran.md` · `…-lensC-seams.md` · `…-lensD-retrogroup.md`
> Source proposal (now superseded on the SET count): `…-container-split-PROPOSAL.md`

## Headline — the fan-out shrank the partition

The S121 proposal (written while the API was down, no independent check) recommended **6 containers**
(`essos, wo5k, north, aegon` + `riverlands` + `kl-faith`, with `iron-islands`/`dorne` floated). **The
independent fan-out refutes the two new ones** and lands on **4**:

- **`riverlands` is OUT.** Lens A: the Stoneheart thread is 2 causally-wired nodes whose upstream root is the
  **Red Wedding** → it is a downstream `[wo5k]` branch, not an independent theater. The Brotherhood arc has
  no decomp and no built junctures — not container-sized.
- **`kl-faith` is OUT.** Lens A: `--causal-chain cersei-is-stripped-and-imprisoned` traces upstream through
  the Tyrion trial → Gregor-confesses → **Purple Wedding** (11 upstream hops). It is a downstream WO5K
  branch. Tag AFFC #1 as `[wo5k]`.
- **`iron-islands` / `dorne`:** small complete sub-arcs (7 / 4 wired nodes) that terminate **into ESSOS**
  (`euron-commissions-victarion`, `death-of-quentyn-martell` already `[essos]`). Lens A: fold as seam nodes,
  don't mint a container. (Lens D treats their AFFC arcs as *gated* — reconciled below: the SET question is
  "are these their own tag, or do they fold into wo5k/essos?")

**This is the single biggest SHAPE finding and the core thing for Matt to ratify or override.**

---

## SHAPE AXIS 1 — THE PARTITION (what is / isn't a container)

**Fan-out consensus: 4 containers.** `{essos, wo5k, north, aegon}` + Jon as a sub-tag (axis 4).

| Container | State | Size evidence |
|-----------|-------|---------------|
| `essos` | BUILT (E1–E5, 15–16 nodes tagged) | the size bar (~8 junctures) |
| `wo5k` | partially built, biggest *built-but-untagged* mass | 13+ nodes; multiple arcs |
| `north` | **greenfield** — same state Essos was at S119 | 4 of 6 key junctures MISS; needs a decomp dip |
| `aegon` | partially built | `landing-of-the-golden-company` has 6 PART_OF sub-beats |

**30 foreshadowed events → home (Lens A):** 11→`[wo5k]`, 5→`[essos]`, 3→`[north]`, 2→`[aegon]`, 2 seams
`[wo5k,north]`, 1 cross-cut `[essos,aegon]`, **6 genuine standalones** (#1 Jon-Arryn, #18 Jaqen-Citadel,
#28 R+L=J, #29 Others'-nature, #30 Doom, #2 Bran's-fall). No event is orphaned.

**Open SET sub-questions for Matt (genuinely undecided):**
1. **Ratify 4, or keep `riverlands`/`kl-faith` as their own tags anyway?** The fan-out's causal argument is
   strong (both root in WO5K). Adopting 4 means the AFFC #1/#3 arcs retro-tag to `[wo5k]`.
2. **`iron-islands` + `dorne`:** fold into existing containers (Lens A: → `essos`/`wo5k` via seam nodes), or
   keep as small standalone tags for retrieval convenience? These are the *only* place the two lenses lean
   differently (A folds; D defers as "gated AFFC arcs"). Low stakes — both are 1-line tag decisions.

---

## SHAPE AXIS 2 — THE BOUNDARIES (root + terminus of the unbuilt containers)

**NORTH** (greenfield, the biggest gap):
- Theater = Watch + wildling + political North. **NOT** "the White Walkers" (sparse in text).
- Root = `jon-joins-the-nights-watch` (**node MISS**); practical causal root shared with WO5K at
  `execution-of-eddard-stark`. Terminus = `jon-is-stabbed-repeatedly` (HIT, 0 causal edges yet).
- 4 of 6 key junctures are MISS → **needs a full decomposition dip before minting** (like Essos at S119).

**AEGON** (partially built):
- Root = Varys/Illyrio tunnel conspiracy (AGOT, Arya witnesses — dyad-queue D1). E7 (Varys/Illyrio)
  **confirmed AEGON**, not Essos (Lens A: JonCon `RESENTS varys` + D1 notation).
- Spine = conspiracy → JonCon/fAegon → Golden Company → `landing-of-the-golden-company` (EXISTS, best
  build-readiness) → Storm's End → `varys-kills-kevan` (#25, MISS).

---

## SHAPE AXIS 3 — SEAMS + BUILD-ONCE OWNERSHIP

**Ownership rule (Lens C, tested on all 13 seam candidates — consistent):**
> The container whose causal **spine directly roots** the node **owns the build**; the other container
> **adds its tag only**.

- **Theon/Reek verdict:** **WO5K owns the build, dual-tag `[wo5k, north]` at the pivot.** Roots in
  `greyjoy-rebellion` (WO5K); `capture-of-winterfell` + `sack-of-winterfell` are the pivot (tag both
  `[wo5k, north]` — they exist but are currently UNtagged). Post-Ramsay-capture nodes are `[north]`-only.
- **Bridge vs seam:** a *bridge* has causal edges crossing the boundary; a pure *seam* is claimed by both
  but causation doesn't cross. Only **one confirmed bridge** today: `robert-orders-daenerys-assassination`
  (correctly `[essos, wo5k]`). `stannis-moves-to-the-wall` becomes the next bridge once built.
- **Pink Letter is NOT a bridge** — `bastard-letter` references WO5K characters but causes only NORTH-internal
  events. Keep `[north]`.
- **Essos∩AEGON seam is premature** — no HotU/Westeros-intent event nodes exist yet. Future seam.

**⚠ Graph-hygiene finding (Lens C, actionable now, independent of the SET):** two AEGON-theater events are
mis-filed `PART_OF war-of-the-five-kings` (a wiki-ingestion artifact): `landing-of-the-golden-company` and
`assassinations-of-pycelle-and-kevan-lannister`. Both should be `containers: [aegon]`, NOT WO5K-scoped. Fix
on the stamp pass.

---

## SHAPE AXIS 4 — GRANULARITY (Jon / Bran)

**Lens B: split treatment — Jon gets the hybrid, Bran gets deferred.**
- **Jon clears the bar** (10 buildable junctures across 42 POV chapters > Essos's ~8). Hybrid dual-tag
  confirmed: AGOT–ASOS Watch-internal beats → `[jon]` only; ADWD LC-era beats (Slynt execution, free-folk
  decision, stabbing) → `[north, jon]` (his authority decisions intersect the political theater).
  `--container jon` and `--container north` return meaningfully different sets — the split prevents pollution.
- **Bran does NOT meet the bar now** (only 4–5 Bran-internal junctures; arc root `jaime-pushes-bran-from-the-tower`
  belongs causally to **WO5K**; greenseer arc is orthogonal to NORTH-political and mostly TWOW).
  **Defer `[bran]`** — name it in the manifest, don't open the dip. Bran's-fall retags `[wo5k]`.
- **Build-order:** Jon J1–J5 are NORTH-independent → can begin immediately. Jon J6–J10 need NORTH *named*
  (not built) first.

---

## SHAPE AXIS 5 (operational) — RETRO-TAGGING THE BUILT ARCS

**Lens D: option (b) — tag the clean `wo5k` subset now, leave AFFC arcs null pending the SET.**
- Half-tagged `wo5k` is **actively worse than none**: `--container wo5k` returns 2 nodes today and looks
  nearly-unbuilt when 13+ exist (Essos shows 16 accurate; wo5k shows 2 misleading).
- **Tag now (zero name-risk, ~13–15 edits via `stamp_containers.py`):** Bran's-fall→`[wo5k]`, Purple Wedding,
  Tywin's death, B1 Red-Wedding-upstream, B3 Ned's-downfall chain, B2 Theon-ward event, battle-of-the-blackwater,
  `littlefinger-betrays-ned` (already stamped). `wo5k` is the most stable name in the project.
- **Gated on the SET:** the 4 AFFC arcs (their tag = whatever Matt decides for kl-faith/riverlands/iron-islands/dorne).
- **Permanently `null`:** Robert's Rebellion, Sack of KL, Greyjoy Rebellion (pre-series history), R+L=J, Doom.
- **Float policy confirmed:** omit key or `null`, **NEVER `[]`**.

---

## What's settled vs what needs Matt

**Settled by the fan-out (high consensus — for Matt to ratify, not re-derive):**
- 4-container partition; NORTH greenfield needs a decomp dip; AEGON spine root = Varys/Illyrio (E7 is AEGON).
- Build-once = spine-root-owns rule; Theon/Reek → WO5K-owned dual-tag.
- Jon = hybrid dual-tag; Bran = deferred.
- Retro-tag the clean `wo5k` subset; the 2 AEGON `PART_OF` misfilings are a fixable hygiene bug.

**Genuinely open — MATT'S CALL (the SET):**
1. **Ratify 4 containers** (drop `riverlands` + `kl-faith` → fold to `wo5k`), or keep them anyway?
2. **`iron-islands` / `dorne`:** fold (into essos/wo5k) or keep as small standalone tags?
3. **Build priority after this** (separate session): WO5K-remainder (safe, built-arc completions) vs NORTH
   (biggest greenfield gap) vs AEGON (partially built). Fan-out leans **WO5K-remainder now while the NORTH
   decomp is written**.
4. **Bran:** confirm defer (name-but-don't-open)?

**NOT this session:** building arcs, tagging containers before the SET is settled.

---

## APPLIED (S122 — Matt decided the SET)

**Matt's SET decision:** adopt **5 containers** `{essos, wo5k, north, aegon, bran}`; **fold** iron-islands/dorne
via seam tags; build **WO5K-remainder** first (next session). kl-faith + riverlands → fold to `wo5k`.

**Bran override (S122):** Matt overrode Lens B's defer. The flight-to-the-north is a container-sized *journey*
arc (fall → Theon-takes-Winterfell → crypts → split from Rickon → north → Nightfort → Coldhands → Bloodraven's
cave; ~8–10 junctures ACOK–ADWD) — Lens B undercounted by scoring only the TWOW greenseer tail. `bran` is now
a confirmed container, but **greenfield** (only 3 Bran-internal event nodes exist; the flight spine is unbuilt
— needs a decomp dip like NORTH/AEGON). Tagged now: `jaime-pushes-bran-from-the-tower` → `[wo5k, bran]` (seam:
WO5K-trigger ∩ Bran-origin), `bran-witnesses-jaime-and-cersei` → `[bran]`, `six-wildling-deserters-ambush-bran`
→ `[bran]`. Deferred to the Bran decomp dip: `bran-s-direwolf-kills-the-assassin` (catspaw bridges to the WO5K
Tyrion-accusation) + the entire unbuilt flight spine.

**Stamps applied via `scripts/stamp_containers.py` (idempotent, frontmatter tags only — no edges/walk touched):**
- **`wo5k` = 24 nodes** (was a misleading 2). The clean Lens-D subset + AFFC #1 Cersei (kl-faith folded)
  + AFFC #3 Stoneheart (riverlands folded): jaime-pushes-bran-from-the-tower, death-of-joffrey-baratheon,
  purple-wedding, assassination-of-tywin-lannister, red-wedding-conspiracy, red-wedding, robb-is-killed,
  execution-of-eddard-stark, arrest-of-eddard-stark, death-of-robert-baratheon, robb-proclaimed-king-in-the-north,
  theon-greyjoy-taken-as-ward, battle-of-the-blackwater, cersei-rearms…, osney-kettleblack-confesses…,
  cersei-is-captured-in-the-sept, cersei-is-stripped-and-imprisoned, catelyn-is-killed,
  catelyn-rises-as-lady-stoneheart, brienne-brought-before-lady-stoneheart (+ littlefinger-betrays-ned
  already + robert-orders… seam).
- **Theon/Reek seam → `[wo5k, north]`:** capture-of-winterfell, sack-of-winterfell (build-once = WO5K-owned).
- **AEGON PART_OF hygiene fix → `[aegon]`:** landing-of-the-golden-company,
  assassinations-of-pycelle-and-kevan-lannister (were mis-filed PART_OF war-of-the-five-kings).
- Verified: `--container wo5k`=24 · `north`=2 (seams) · `aegon`=2 · `essos`=16 (unchanged). Genuine
  standalones (RR, Sack-of-KL, Greyjoy-Rebellion, R+L=J, Doom) left `null` permanently.

**Deferred to the relevant build session (NOT WO5K-remainder critical path) — iron-islands/dorne fold interiors.**
"Fold via seam tags" settled the SET; the interior beats' *causal home* is genuinely ambiguous (Kingsmoot
interior feeds Essos; Dorne interior's upstream is WO5K via the Sand-Snakes arrest, downstream bridges to
AEGON) — don't bake in a boundary guess. Existing interior slugs to settle then:
- **Iron Islands → likely `[essos]` at the bridge:** `euron-commissions-victarion-to-fetch-daenerys`
  (the Essos bridge), death-of-balon-greyjoy, euron-seizes-the-seastone-chair, kingsmoot-on-old-wyk,
  taking-of-the-shields, asha-claims-the-kingsmoot, euron-hunts-aeron-damphair, et al.
- **Dorne → settle when AEGON is built:** the-queenmaker-plot, areo-hotah-springs-the-ambush,
  arianne-collapses-and-is-captured, myrcella-is-maimed-by-darkstar; `arrest-of-the-sand-snakes` =
  `[wo5k]` seam (Oberyn-death upstream); `doran-reveals-fire-and-blood-pact` = the AEGON bridge.
- `death-of-quentyn-martell` already `[essos]` — no action.
