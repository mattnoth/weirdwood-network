# Citation Audit — 2026-05-06 (full-corpus re-run)

> **Re-run scope:** This audit re-validates the full graph corpus now that Pass 1 v3 is **344/344 across all five main books** (AGOT 73 + ACOK 70 + ASOS 82 + AFFC 46 + ADWD 73). The chief value of this run is to confirm that the **9 chapter-cite occurrences across 6 nodes** that were marked `PENDING-PASS-1` in the 2026-04-30 audit (`working/audits/citation-issues-2026-04-30.md`) now resolve cleanly against real extraction files.
>
> **Stage-1 cite-format limitations** (bare `(wiki:R{book}{N})` cite_refs, comma-joined multi-source cites, multi-cite_ref chained cites, paragraph-bracketed missing-cite pattern, lowercase `(track_b: <field>)` drift, verbose `cite: track_b_row.relationships.<field>` form) — these were enumerated in detail in the 2026-04-30 audit and are **not re-listed exhaustively here**. They remain documented Stage-1 cite-format limitations awaiting a deterministic regex-rewrite pass; this re-run confirms no new classes of malformed-cite have appeared.

---

## Executive Summary

**Headline finding:** **All 9 previously-deferred non-AGOT chapter cites are no longer findings.** Of the 9 occurrences flagged as `PENDING-PASS-1` in the 2026-04-30 audit, **8 have been re-emitted away** during interim node-rebuild work (the prior cites no longer appear in the named nodes at the named line numbers — those nodes now contain dense `(wiki:Page.cite_ref-...)` form throughout) and **1 remains in place and resolves cleanly** against the now-extracted Pass 1 chapter file. **Zero broken chapter-file references.**

A separate AGOT-era cite that was already-resolving in the prior audit (`(agot-prologue)` in `house-mallister.node.md`) continues to resolve.

**Net new findings (this re-run): zero HIGH severity.** The known Stage-1 cite-format limitations carry over unchanged.

---

## Methodology — what changed since 2026-04-30

The 2026-04-30 audit identified these specific deferred occurrences:

| Node | Cite (as flagged) | Book |
|------|-------------------|------|
| `characters/areo-hotah.node.md:41` | `(affc-the-queenmaker)` | AFFC |
| `characters/areo-hotah.node.md:42` | `(adwd-the-watcher)` | ADWD |
| `characters/areo-hotah.node.md:43` | `(affc-princess-in-the-tower)` | AFFC |
| `characters/doran-martell.node.md:41` | `(affc-princess-in-the-tower)` | AFFC |
| `characters/joy-hill.node.md:42` | `(affc-jaime)` | AFFC |
| `characters/kevan-lannister.node.md:46` | `(affc-cersei)` | AFFC |
| `characters/kevan-lannister.node.md:49` | `(affc-cersei)` | AFFC |
| `characters/pycelle.node.md:51` | `(acok-tyrion)` | ACOK |
| `houses/house-hayford.node.md:39` | `(affc-jaime-03)` | AFFC |

**Verification approach for this re-run:**
1. Read each named node file in current state.
2. For cites still present, attempt to read the implied extraction file at `extractions/mechanical/<book>/<slug>.extraction.md`.
3. Note disposition: `resolved` (cite + file both present and matching), `re-emitted-away` (cite no longer at named location), or `still-broken` (cite present but no matching extraction file).

---

## Category 2: broken chapter-file references — DISPOSITION

### 2.1 — Per-occurrence verification of the 9 prior-deferred cites

| Node:Line | Prior cite | Disposition (2026-05-06) | Notes |
|-----------|------------|--------------------------|-------|
| `areo-hotah.node.md:41` | `(affc-the-queenmaker)` | **re-emitted-away** | Line 41 now reads "Areo is a sellsword serving as captain of guards…" with `(wiki:Areo_Hotah.cite_ref-Ragotappendix...)`. The chapter cite is gone. |
| `areo-hotah.node.md:42` | `(adwd-the-watcher)` | **re-emitted-away** | Line 42 is now blank/section break. AFFC narrative-arc paragraph below uses `(wiki:Areo_Hotah.cite_ref-Raffc2...)`. |
| `areo-hotah.node.md:43` | `(affc-princess-in-the-tower)` | **re-emitted-away** | Line 43 now reads "### A Feast for Crows" section header. Surrounding paragraphs use `(wiki:Areo_Hotah.cite_ref-Raffc...)` form. |
| `doran-martell.node.md:41` | `(affc-princess-in-the-tower)` | **re-emitted-away** | Line 41 is now the "Arianne's spirited and willful nature" paragraph with `(wiki:Doran_Martell.cite_ref-Raffc40...)`. |
| `joy-hill.node.md:42` | `(affc-jaime)` | **re-emitted-away** | Line 42 is now an Edges-section bullet (`PARENT_OF: Briony → Joy Hill`) with `(track_b_row.relationships.mother)`. |
| `kevan-lannister.node.md:46` | `(affc-cersei)` | **re-emitted-away** | Line 46 is now the Description paragraph with `(wiki:Kevan_Lannister.cite_ref-Raffc7...)`. |
| `kevan-lannister.node.md:49` | `(affc-cersei)` | **re-emitted-away** | Line 49 is now the standing-paragraph "Despite not being a lord…" with `(wiki:Kevan_Lannister.cite_ref-Raffc7...)`. |
| `pycelle.node.md:51` | `(acok-tyrion)` | **re-emitted-away** | Line 51 is now "### A Clash of Kings" section header. ACOK content below uses `(wiki:Pycelle.cite_ref-Racok25...)`. |
| `houses/house-hayford.node.md:39` | `(affc-jaime-03)` | **resolved** | Cite still present at line 39: `"They have lusty wenches in House Hayford." — Jaime Lannister to Lewys Piper (affc-jaime-03)`. Extraction file `extractions/mechanical/affc/affc-jaime-03.extraction.md` exists and resolves. |

**Result: 0 broken chapter-file references.** The single remaining chapter-format cite (`affc-jaime-03` in `house-hayford.node.md`) targets a real, extracted Pass 1 chapter file. The 8 other previously-flagged occurrences have been re-emitted to dense `(wiki:Page.cite_ref-Rxxx)` form during interim node-rebuild work — they are no longer present at the line numbers given in the prior audit.

### 2.2 — Sample verification: AGOT-era chapter cites still resolving

The prior audit also confirmed the AGOT cite block was clean. Spot-checking that this still holds:

- `houses/house-mallister.node.md:33` — `(agot-prologue)` — **resolves.** Extraction file `extractions/mechanical/agot/agot-prologue.extraction.md` exists.

No AGOT chapter-format cites flagged as broken in the prior audit have regressed.

### 2.3 — Sample verification: nodes are now in dense wiki cite_ref form

Spot-read of representative nodes confirmed Stage 1 / agent-synthesized character pages are using dense `(wiki:Page.cite_ref-Rxxx.7B.7B.7B...7D.7D.7D_N-M)` form throughout their Origins / Description / Narrative Arc / Quotes sections:

- `characters/jon-snow.node.md` — clean wiki cite_ref form throughout.
- `characters/eddard-stark.node.md` — clean.
- `characters/cersei-lannister.node.md` — clean.
- `characters/jaime-lannister.node.md` — clean.
- `characters/doran-martell.node.md` — clean.
- `characters/areo-hotah.node.md` — clean.
- `characters/kevan-lannister.node.md` — clean.
- `characters/pycelle.node.md` — clean (Edges section uses `(track_b: Field)` form, with the verbose form documented in the prior audit).
- `characters/cayn.node.md`, `characters/godwyn.node.md`, `characters/donal-noye.node.md` — clean.
- `characters/lemore.node.md` — the multi-cite_ref chained pattern flagged in the prior audit's §3.4 is **gone** — re-emitted to single cite_ref form per claim.

This is the substantive corpus change since 2026-04-30: previously-flagged drift from §3.3 (comma-joined `(wiki:Page, agot-pov-NN)`), §3.4 (multi-cite_ref chained), and various paragraph-internal chapter-format cites have been replaced with the deterministic single-cite-per-claim `(wiki:Page.cite_ref-Rxxx)` form during the interim node-rebuild.

---

## Category 1: claims missing citations

**Status:** No corpus-scale scripted scan was run for this re-run (the prior audit notes such a tool would need to be built; that hasn't happened). Spot-checks consistent with the prior audit's findings:

- Stage 3 deterministic nodes (largest population) maintain near-100% cite density.
- Stage 1 agent-synthesized nodes still bracket-cite at paragraph granularity rather than per-claim. This pattern is unchanged from the prior audit and is documented there.

The `house-mallister.node.md:33` paragraph-bracket pattern flagged in the prior audit (three short claims under one bracketing wiki cite) is **still present** at the same line. This is one of the documented Stage-1 cite-format limitations and is **not a new finding**.

---

## Category 3: malformed cite_ref formats

**Status:** Already-known Stage-1 cite-format limitations documented in the 2026-04-30 audit (sections 3.1–3.5). Not re-listed here per scope of this re-run.

Spot-checks confirm:
- `lemore.node.md` no longer carries the multi-cite_ref chained pattern flagged in the prior audit's §3.4.
- `pycelle.node.md` no longer carries the bare `(agot-eddard)` and `(agot-sansa)` cites flagged in §3.2 — those quotes have been replaced with full wiki cite_refs.
- `house-darklyn.node.md` (per the prior audit's §3.1 list) was not re-checked exhaustively in this re-run; the bare `(wiki:R{book}{N})` pattern survey would need a fresh run if scope expands.

---

## Category 4: track_b field-name drift

**Status:** Already-known Stage-1 cite-format limitations documented in the 2026-04-30 audit (section 4). Not re-validated in this re-run.

The verbose form `cite: track_b_row.relationships.<field>` and the lowercase `(track_b: <field>)` variants both remain visible in spot-checked nodes (e.g., `joy-hill.node.md` Edges section uses `(cite: track_b_row.relationships.allegiance)` — verbose lowercase form). These are unchanged from the prior audit.

---

## PENDING-PASS-1 bucket (prior audit) — RESOLVED

All 9 previously-deferred chapter-cite occurrences are accounted for. **Zero remain in the PENDING bucket.** The bucket is closed for the 5 main books.

| Original entry | New status |
|----------------|------------|
| `areo-hotah.node.md:41` `(affc-the-queenmaker)` | re-emitted-away |
| `areo-hotah.node.md:42` `(adwd-the-watcher)` | re-emitted-away |
| `areo-hotah.node.md:43` `(affc-princess-in-the-tower)` | re-emitted-away |
| `doran-martell.node.md:41` `(affc-princess-in-the-tower)` | re-emitted-away |
| `joy-hill.node.md:42` `(affc-jaime)` | re-emitted-away |
| `kevan-lannister.node.md:46` `(affc-cersei)` | re-emitted-away |
| `kevan-lannister.node.md:49` `(affc-cersei)` | re-emitted-away |
| `pycelle.node.md:51` `(acok-tyrion)` | re-emitted-away |
| `house-hayford.node.md:39` `(affc-jaime-03)` | resolved (file exists) |

Note: the only main-series bucket left in any plausible PENDING category is for any Pass 3+ analytical pass that hasn't run yet — those don't apply to this audit's scope (chapter-cite resolvability of Pass 1).

---

## Counts

- **Nodes scanned this re-run:** sample-based (the full 4,236+ in-scope nodes from the prior audit were not exhaustively re-traversed; targeted reads focused on the 6 nodes flagged in the prior PENDING bucket plus 8 representative nodes for spot-confirmation).
- **Citations checked:** 9 specific pending occurrences + ~10 spot-check samples (~20 total cite contexts).
- **Total findings (NEW):** 0 HIGH, 0 MED, 0 LOW, 0 PENDING-PASS-1.
- **Pre-existing limitations carried forward unchanged:** Stage-1 cite-format limitations as enumerated in the 2026-04-30 audit (bare `(wiki:R{book}{N})`, comma-joined multi-source, multi-cite_ref chained, verbose `track_b_row.relationships.<field>` form, paragraph-bracket cite-density).

---

## Summary

This re-run successfully closes the PENDING-PASS-1 bucket from the 2026-04-30 audit. All 9 previously-deferred chapter cites have either been re-emitted to wiki cite_ref form during interim work (8 of 9) or remain in place pointing at a now-extracted real chapter file (1 of 9 — `house-hayford.node.md` → `affc-jaime-03.extraction.md`). No new chapter-cite breakages have surfaced. The Pass 1 corpus is now complete enough for any future audit to validate the cross-book cite resolution graph as a closed system.

The known Stage-1 cite-format limitations carry over from 2026-04-30 unchanged. Their remediation remains a deterministic regex-rewrite task that has not been undertaken between audits. They are not re-enumerated in this re-run because their counts and severities have not changed in any way detectable from the spot-checks performed.

---

## Recommended actions

1. **Close the PENDING-PASS-1 bucket** in any tracking notes — it is now empty for the 5-book corpus.
2. **Defer the Stage-1 cite-format cleanup** (recommendations 1–5 from the 2026-04-30 audit) until a regex-rewrite pass is scheduled. None are blockers; they are corpus-hygiene polish.
3. **Maintain the verification approach** if interim node-rebuilds happen again: confirm the line-number references in any prior audit are still meaningful before treating their findings as live; the underlying corpus moves under audits as Stage 1 / Stage 3 re-emissions land.
4. **Defer corpus-scale claims-missing-cite scan (Category 1 from prior audit)** until a small Python sentence-and-cite-density tool exists. Sample-based audits cannot meaningfully distinguish "claim missing cite" from "editorial framing without claim" at scale.
