# Session 122 — Container-SHAPE analysis (the fan-out that overturned the proposal) + SET decision + Bran override

**Date:** 2026-06-21 → 06-22
**Model:** Opus 4.8 orchestrator + 4 Sonnet 4.6 `general-purpose` lens subagents (read-only). No build subagents (shape session).
**Type:** Design/decision session — warranted a detail file (the SET is a graph-shape decision; the fan-out refuted the prior draft).

---

## Purpose

The dedicated container-SHAPE session Matt asked for at S121. S121's Step-2 container-split fan-out had been
**blocked by a persistent Anthropic 529 overload** (all 4 lens subagents died, 0 tool uses), so the S121
orchestrator wrote a *stand-in proposal* in-house and flagged it as needing independent pressure-testing.
This session ran that fan-out (API healthy) and settled the shape.

**Governing principle (carried from S121): SHAPE > NAMES.** Container tags are trivially reversible
(`stamp_containers.py` find-replace, touches no edges/walk/derived artifacts), so names stay provisional.
The *expensive* axes — partition / boundaries / seams+ownership / granularity — are what the session had to
get right, because arcs get built under them.

---

## What happened

### 1. API probe → fan-out
One trivial probe agent returned HEALTHY (no 529). Dispatched the 4 read-only Sonnet lenses in parallel,
each reading the pre-written `…-container-split-BRIEFING.md` and pressure-testing the
`…-container-split-PROPOSAL.md` rather than echoing it. All 4 completed (66/76/57/49 tool uses).

### 2. The fan-out OVERTURNED the proposal's headline
The S121 proposal (written blind) recommended **6 containers** — adding `riverlands` + `kl-faith` to the
board's NORTH+AEGON. The independent lenses **refuted both** with causal evidence:
- **`kl-faith` OUT** — Lens A ran `--causal-chain cersei-is-stripped-and-imprisoned`: it traces **11 hops
  upstream to the Purple Wedding**. Cersei's downfall is a downstream WO5K branch, not an independent theater.
- **`riverlands` OUT** — the Stoneheart thread is 2 nodes rooted in the Red Wedding → WO5K.
- **`iron-islands` / `dorne`** — small complete sub-arcs that terminate into Essos; fold via seam tags.

This is the value of the fan-out: the pressure-test caught an over-partition the blind draft would have baked in.

### 3. The four shape axes (lens consensus)
- **Partition** — 4 containers `{essos, wo5k, north, aegon}`; all 30 foreshadowed events have homes; 6 genuine
  standalones stay `null`.
- **Boundaries** — NORTH greenfield (4/6 junctures missing, needs a decomp dip); AEGON spine root = the
  Varys/Illyrio conspiracy; **E7 confirmed AEGON not Essos**.
- **Seams** — build-once = *the container whose causal spine roots the node owns the build*; Theon/Reek →
  WO5K-owned, dual-tag `[wo5k, north]` at the capture/sack-of-Winterfell pivot. One true bridge today
  (`robert-orders…`). Pink Letter is *not* a bridge. Lens C also caught a real **graph-hygiene bug**:
  `landing-of-the-golden-company` + `pycelle/kevan-assassinations` are mis-filed `PART_OF war-of-the-five-kings`
  (wiki-ingestion artifact) — they're AEGON-theater events.
- **Granularity** — Jon = hybrid dual-tag (clears the ~8-juncture bar at 10); Bran = *Lens B said defer*.

### 4. Matt's SET decision (shape-first; Matt decides, orchestrator did not)
Via AskUserQuestion (Matt chatted Q1 first — "why is less containers better?" — answered: a container should
mark an *independent causal origin*, not a downstream branch; fewer keeps `--container` honest; under-partition
is the safe direction because folding-now/carving-later is cheap while splitting-then-merging is rework):
- **Adopt 4** `{essos, wo5k, north, aegon}` — kl-faith + riverlands fold to `wo5k`.
- **Fold** iron-islands/dorne via seam tags.
- **Build WO5K-remainder first** (next session; seam-safe, no decomp dip needed).

### 5. Bran override (Matt, post-decision)
Matt overrode Lens B's defer: *"Bran's whole flight to the north is worth something."* He's right — Lens B
undercounted by scoring only the TWOW greenseer tail; the **flight itself** (fall → Theon takes Winterfell →
crypts → split from Rickon → north → Nightfort → Coldhands → Bloodraven's cave) is an 8–10 juncture *journey*
arc spanning ACOK–ADWD, container-sized by the Essos bar. So **`bran` is the 5th container** — but greenfield
(only 3 Bran-internal event nodes exist; the flight spine is unbuilt). Needs a decomp dip like NORTH/AEGON.

### 6. Mechanical stamps applied (post-decision, the STEP-3 mechanical step)
All via `scripts/stamp_containers.py` (idempotent, frontmatter tags only — no edges/walk/derived touched):
- **`wo5k` = 24 nodes** (was a misleading 2 — the half-tagged problem Lens D flagged). The clean Lens-D subset
  + AFFC #1 Cersei (kl-faith folded) + AFFC #3 Stoneheart (riverlands folded).
- **Theon/Reek seam → `[wo5k, north]`:** capture-of-winterfell, sack-of-winterfell.
- **AEGON PART_OF hygiene fix → `[aegon]`:** landing-of-the-golden-company, assassinations-of-pycelle-and-kevan-lannister.
- **`bran` = 3 nodes:** jaime-pushes-bran-from-the-tower → `[wo5k, bran]` (seam), bran-witnesses-jaime-and-cersei +
  six-wildling-deserters-ambush-bran → `[bran]`.
- Verified: `--container` wo5k=24 · essos=16 (unchanged) · north=2 · aegon=2 · bran=3.

### Deliberately deferred (boundary-ambiguity discipline)
- **iron-islands/dorne fold interiors** — the SET is decided but the interior beats' *causal home* is genuinely
  ambiguous (Kingsmoot feeds Essos; Dorne's upstream is WO5K, downstream bridges to unbuilt AEGON). Left a
  precise slug list in the SHAPE map for the relevant build session rather than bake in a boundary guess. The
  Euron bridge is `euron-commissions-victarion-to-fetch-daenerys` (not the slug the proposal cited).
- **AEGON `PART_OF` edge** — only the container *tag* was fixed; the wrong `PART_OF war-of-the-five-kings`
  *edge* is a separate hygiene cleanup for the AEGON build.

---

## Outcome / what's next
Shape settled (5 containers), stamps applied + verified, no node/edge mints (tags only). The next session is a
**build session: WO5K-remainder** (Q5 → J2+J9 → J7 → J4 per `working/wo5k-decomposition.md`). Continue prompt
`progress/continue-prompts/2026-06-22-wo5k-remainder-build.md`. Bran + NORTH + AEGON each queued behind it,
each needing its own decomp dip first.

## Artifacts
- `working/session-results/2026-06-21-container-SHAPE-map.md` — the synthesis (4 shape axes + APPLIED section).
- `working/session-results/2026-06-21-container-split-lens{A,B,C,D}-*.md` — the 4 lens reports.
- `progress/continue-prompts/2026-06-22-wo5k-remainder-build.md` — next build session.
