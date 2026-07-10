# SESSION 206 — Cross-era seams: wire the F&B/Targaryen-history layer to the main-series (GoT-era) graph

> **This is Session 206.** Stamp your worklog entry `### Session 206` at endsession.
> **Recommended model:** **Sonnet 4.6** — arc-enrichment-style: Sonnet orchestrator + Sonnet
> proposer lenses + Haiku/Sonnet fresh-verifiers (the S133–S167 enrichment machine). Quote-grounded,
> fresh-verified. This is a *seam-wiring* dip, not a mass mint.
> **PRE-REQ:** S205 (harvest drain) committed+pushed. If `git log` disagrees with worklog.md S205, STOP and reconcile.

## Why (Matt-sequenced)
The S200–S204 work built a whole Fire & Blood / Targaryen-history layer (event nodes, causal spine,
quotes). It is currently **an island**: a show-watcher asking a Dance question can walk *within* the
F&B era (S204 gave it a causal spine) but cannot walk **into** the main-series (GoT-era) graph, and a
main-series reader can't reach back. Matt: "we will need to backfill some game of thrones edges with
the new ones." Persistent entities and textual references straddle both eras — wire them **both
directions** so traversal crosses the ~170-year gap.

## The task — seam-wiring (arc-enrichment machine)
Wire edges connecting the F&B/Targaryen-history layer to the existing main-series graph. Candidate seams
(verify each against LOCAL cache — `sources/wiki/_raw/` + book chapters — before minting; quote-ground
Tier-1/Tier-2):
- **Persistent artifacts:** `blackfyre` (Aegon I's sword → Daemon Blackfyre → Blackfyre pretenders →
  Bittersteel carries it to the Golden Company; also lost) and `dark-sister` (Visenya → Daemon →
  Bloodraven → beyond the Wall). These VS swords thread F&B → D&E → main-series. Wire holder/lineage
  chains (`REFORGED_INTO`? no — same swords; use OWNS/WIELDS/GIFTED_TO/LOOTED_BY across holders).
- **Dragonstone** (`dragonstone`): Targaryen seat across all eras — F&B ↔ main-series (Stannis).
- **Dragon skulls** in the Red Keep throne room (main-series) ← the F&B dragons (Balerion/Vhagar/etc.).
- **Textual references** in main-series to the Dance / Targaryen history: maester lore, "the dragons
  danced and men died," Dany's House-of-the-Undying visions, Old Nan's tales. Wire `FORESHADOWS` /
  `PARALLELS` / `DEPICTED_IN` where the text supports it.
- **CONSIDER D&E** (`tmk`/`tss`/`thk` — **no Pass 1, read the chapter files directly**): Blackfyre
  Rebellions, Bittersteel, Bloodraven, the Golden Company origin — these are the natural F&B ↔ main
  bridge and much is already node-present from the wiki layer.

## ALSO absorb the S204 + S205 residue flags (todos)
- `lord-rogars-war` vs `third-dornish-war` — suspected **duplicate nodes**; check + merge if same.
- Mistyped nodes: `maidens-day-ball` / `regency-of-aegon-iii` typed `event.battle`; `archon-of-tyrosh-war-of-the-ninepenny-kings` (`event.war` used as a person). Retype.
- Backwards wiki edge: `assault-on-harrenhal DEFEATS blacks` — direction wrong; fix.
- Unminted flagged beats (optional mints if a seam needs them): Prince Daeron the Daring's death at
  Second Tumbleton (3 conflicting accounts — death account already on `daeron-targaryen-son-of-viserys-i`
  ## Quotes from S205; the `death-of-daeron-targaryen-son-of-viserys-i` **event** node is still a
  candidate mint); Prince Gaemon birth/death.

## Machine (the enrichment dip pattern)
1. **Baseline probe:** for each candidate seam entity, `weirwood query neighbors <slug>` + check whether
   a cross-era edge already exists (dedup — many may be wiki-present). Read LOCAL cache to ground.
2. **Propose:** Sonnet lens(es) propose seam edges with verbatim quote grounding (book or wiki cite_ref).
   Mint via `scripts/mint_enrichment.py --candidates …`.
3. **Fresh-verify** a fresh Sonnet/Haiku pass on every proposed edge (adversarial; the S133+ standard);
   orchestrator adjudicates each non-CONFIRM with the source open.
4. **Finalize** via `scripts/finalize_enrichment.py --verdicts …`; `weirwood refresh` (nodes added →
   needed); gate + pytest/deno; **STEP-0 harvest consume** of any new harvest rows this dip drops.
5. **Capture quotes** while in the text (FIRM rule) — drop harvest pointers for out-of-scope finds.

## Success criteria
- `walk_chain` / `neighbors` cross the era boundary on ≥1 marquee case (e.g. `blackfyre` walks F&B →
  Golden Company / AEGON arc; a Dance reference reachable from a main-series node).
- All new edges quote-grounded + fresh-verified; the 3–4 S204 residue hygiene items resolved.
- Gate PASS; suites green; harvest queue drained at endsession (≥30 bar).

## DO NOT
- Do NOT re-run extraction. Do NOT start theories (theory-gated) or the strip track (Matt-gated).
- Do NOT mass-mint — this is seam-wiring; dedup hard against the existing (wiki-heavy) graph first.
- Do NOT auto-run /endsession.

## Backlog (NOT this session unless Matt asks) — from S205 residue
- **~85 nodes graph-wide carry duplicate `## Quotes` headers** — `parse_quotes` reads only the first,
  so second-section content is invisible to the chat/bundle. Scriptable merge-fix (a schema-drift dedup
  pass). Scan: `for f in $(grep -rl '^## Quotes' graph/nodes/); do [ $(grep -c '^## Quotes' "$f") -ge 2 ] && echo "$f"; done`.
- Edge-vocab retrofit (Matt's original backfill idea) rides AFTER seams.
