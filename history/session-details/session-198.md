---
session: 198
date: 2026-07-06
track: graph
model: Opus 4.8 (orchestrator) + 5× script-builder subagents (Sonnet-class) + 1 fresh general-purpose evaluator
title: Fire & Blood ingestion pipeline — built end-to-end + first-ever smoke run
---

# Session 198 — Fire & Blood pipeline build + Stage-1 smoke

## Purpose
Execute the F&B build (design `working/fire-and-blood/fire-and-blood-enrichment-design.md` v2, GO-WITH-CHANGES
from the S196 Fable review): build the whole node-first enrichment pipeline, then run the Matt-fired Stage-1
smoke. Extraction = the *output* of the build, not parallel-startable. Node writes stay gated.

## What the pipeline is (plain terms)
An assembly line that upgrades the graph's thin, wiki-derived Targaryen-history layer to Tier-1 book-cited
provenance (and mints net-new F&B figures/events). ~70% UPDATE existing nodes, ~30% CREATE. HotD is airing →
high portfolio value. Four stages: split the epub → Opus reads each chunk → deterministic reconciler resolves
names→slugs (the danger zone) → merge writer folds book prose into existing nodes.

## Build decisions & discoveries (the judgment work)

**The epub `toc.ncx` is unreliable.** Several navPoints point at `index_split_000.html#page_N` anchors that
resolve nowhere (Calibre garbage); files 011/014 have no navPoint at all (mid-sentence continuations). So I
hand-verified all 23 sections against the unzipped HTML and wrote an authoritative `working/fire-and-blood/
unit-map.json` (section→file→unit, era, dance-core flags, wiki section-slugs, title-marker kinds). Section titles
are encoded three ways (`<p id=page_N><span class=calibre3>`, `<h2>`, or none-for-continuations); the leaked PDF
build-path artifact lives in `<head><title>` (strip the head, not body prose). File 003 has an OCR-garbage
"Dedication" preamble before the real Aegon's-Conquest marker — dropped by starting at the title anchor.

**NN convention = HTML file number, 2-digit.** The design's prose said "NCX section order" but its worked
examples (`fab-aegons-conquest-03`, `fab-heirs-of-the-dragon-15`) and the smoke-unit names use the HTML file
number. NCX playOrder ≠ file number (Aegon's Conquest is playOrder 2 but file 003), so the worked examples win.
Chapter files use 2-digit NN (cite_refs bake it in); candidate packs came out 3-digit (`…-015.json`) — the
reconciler/worker bridge this by matching on the unit **slug**, not the zero-padded NN. Cosmetic, handled.

**The R1 confident-wrong-match trap is real and live.** `weirwood query resolve "Aegon Targaryen"` STILL returns
a confident `HIT-CHARACTER` on `aegon-targaryen` — a zero-edge junk node minted from the wiki's *disambiguation
page*. Naive MATCH-first would pour Aegon II's biography onto it and silently corrupt the graph. The reconciler's
job #1 is to consult the S197 blocklist + same-name clusters + redirect map and route any such hit to review.
**Independently re-verified on real smoke data: 0 trap edges, 0 trap merges.**

## Components built (all self-verified; 5 script-builder subagents + me on prompt/map/arch-batch)
1. `scripts/fire-and-blood-splitter.py` → `sources/chapters/fab/` — 23 sections → **39 unit files**; QA gate 0
   warnings (0 PDF-path leaks / 0 word-miss / 0 boundary dupes); `ocr-scan.md` flags the OCR-hot files (025
   Lineages 275, 012 111, 014 108 — matches the design's prediction). NOT frozen (Matt's gate).
2. `scripts/fab-build-candidate-packs.py` → 23 packs, 1,526 nodes mapped from `Rfab` cite anchors; 015-pack
   acceptance PASS (rhaenyra/daemon/criston). 4 unmapped section slugs, all typo noise (1–2 nodes each).
3. `working/fire-and-blood/prompts/fab-enrichment-v1.md` — node-first schema (roster+prose+edges+events+harvest);
   descends from D&E v4 (self-contained, locked vocab, harvest sidecar, no-meta-commentary, forward-only); NEW:
   node-prose output, mandatory Disambiguator column, OCR dual-rule (canonical-in-roster / verbatim-in-quotes),
   Gyldayn dispute model (`in_universe_source` + `disputed`).
4. `scripts/fab-reconcile-candidates.py` — the crux. Parses proposal → routes names (UPDATE/CREATE/review) via
   resolver + blocklist + clusters + redirect map + candidate-pack prior + discriminator scoring (≥2-independent
   + decisive-margin auto-accept, disabled under `--smoke`); quote pre-validation (norm+grep, row-level
   quarantine, never abort); `disputed ⇒ tier-2` invariant; emits candidates.json + merge-plan.json +
   contradictions-report + run-summary + 3 review files; CREATE nodes stamp `era`/`occurred`. 6/6 unit assertions
   pass incl. the trap tests.
5. `scripts/fab_merge_node.py` — the NEW UPDATE writer (mint is skip-if-exists). Handles all 3 node shapes +
   both (c) sub-cases; boilerplate Identity-line swap only on true stubs; rhaenyra's ~90 lines of wiki prose
   byte-identical; idempotency marker + hard-error-on-not-found (R3 defense). Smoke-passed on copies.
6. `working/fire-and-blood/fire-and-blood-extraction.py` — long-run worker, mirrors D&E. 39-unit queue + roster
   hints + placeholder substitution + safety guard (real `claude -p` only on --smoke/--resume). Registered
   `PLANNED` in `weirwood-run.sh` (D&E precedent — a working/ scaffold shouldn't be READY).

Staged (Matt-gated, lands WITH first apply): `working/fire-and-blood/architecture-batch-s198.md` — `fab` code,
`book-fab` evidence_kind, `in_universe_source`/`disputed` edge fields, the tier invariant, + the 3-line mint
passthrough patch.

## Stage-1 smoke (Matt fired from iTerm — first-ever completed run of the `claude -p`+`longrun.sh` pattern)
Unit `fab-aegons-conquest-03`. Output: 40KB, 350 lines, all 5 headers. Reconciler on the real output:
- 148 entities → 39 matched / 108 review (auto-accept disabled under --smoke — expected) / 36 created
- 58 edge candidates (healthy vocab spread: PARENT_OF/SIBLING_OF/SPOUSE_OF/KILLS/AGENT_IN/VICTIM_IN/…)
- 135 quotes, **89.6% located**, 14 quarantined (just under the 90% gate — OCR-attention flag)
- disputed_rate 3.4% (plausibly low for mostly-uncontested Conquest narration)
- **0 trap edges / 0 trap merges** — R1 holds on real data
Fresh-agent evaluation (a general-purpose subagent, since the builder shouldn't grade the pipeline):
**VERDICT = PASS-WITH-CONCERNS** (`working/fire-and-blood/smoke/v1/EVAL-stage1.md`). The extraction half is
**strong — ship the prompt as-is** (roster full + correctly disambiguated `Aegon I` vs `Aegon son of Gaemon`;
prose factual/budget-respecting/no banned words/no invented facts; edges LOCKED-vocab + correct agent-direction
+ qualifiers; quotes verbatim with garbles intact; disputed_rate 0.034 correctly calibrated — only 2 real hedges,
both tier-2 `unattributed`; the 14 quarantines are **100% line-wrap false-negatives, 0% fabrication**). But the
**reconciler has a CREATE-routing bug class that WOULD corrupt the graph if applied** (dry run — nothing minted):
1. **CREATE guard too weak (BLOCKER):** ~9 house dupes (`blackwoods`→existing `house-blackwood`), + `daenys`→
   `daenys-targaryen`, `arrec`→`arrec-durrandon` minted despite the resolver returning fuzzy `candidates` —
   design §5.1 rule 3 says route those to review, not CREATE. The reconciler is treating status `candidates` as
   a clean miss.
2. **Composite/collective cells minted as nodes (BLOCKER):** 7 junk `character.human` nodes from unsplit
   `;`-joined Event-table cells (`mern-ix-gardener-loren-i-lannister`) + collectives (`the-targaryen-fleet`).
3. **Quote locator misses paragraph-spanning quotes (HIGH, cheap):** all 14 quarantines recover under
   whitespace-collapse; the locator joins only 2 physical lines. **Fix must be mirrored in `mint_enrichment.py`'s
   `authoritative_line` identically** — else a reconciler-located quote aborts mint (they must stay lockstep).
4. Contradictions report polluted by the dupe bug (re-diff after fix).
5. New-node type defaults to `character.human` instead of carrying the extractor's Type-guess column.
**Net:** ~18 dupe/junk nodes + fractured kinship edges IF applied — but nothing is. All blockers are deterministic
reconciler fixes. After fix, re-run reconcile on this unit (CREATEs 36→~14, quarantine→~0), THEN Stage 2. R1
held perfectly (0 trap edges/merges).

## Process notes
- 5 script builds delegated to `script-builder` (2-3 concurrent, named-file outputs, verify-on-resume). No graph
  or edges.jsonl mutation all session. All 5 scripts compile; reconciler→mint→merge schema handoff confirmed.
- `claude -p` 401s from inside Claude Code (OAuth not inherited) → smoke is Matt-fired from iTerm (durable
  finding; `feedback_no_extraction_without_asking`). Runs on Matt's subscription, not a metered API key.
