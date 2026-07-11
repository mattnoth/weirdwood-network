# Session 209 — Draining the 76 dispute-held recovery rows

**Date:** 2026-07-11 · **Model:** Opus 4.8 orchestrator · **Track:** graph (Fire & Blood)
**Scope:** the LAST open step of the review-bucket recovery track. Graph mutation: YES.

## Goal

The S208 review-bucket recovery landed 995 edges + 201 event nodes from the 1,440
quarantined rows, but **76 recovered rows were held** by the reconciler's §7.2
hedge-proximity quarantine (`recovery-s208/out/*/dispute-review.jsonl`) instead of landing.
This session drained them via the S201 machinery: `fab-dispute-preclassify` →
primary-text adjudication of the residue → `fab-dispute-inject` → mint + merge → gates.

## Row shape and preclassification

76 rows = 47 edge + 24 prose + 5 event. Every row carried a `hedge_term`
(mushroom / eustace / avers / "can be believed") — the reason it was quarantined — but in
Fire & Blood those terms are chronicler *names*, and the quarantine fires on mere paragraph
proximity. So the working hypothesis (borne out completely) was that the holds are
false-positives.

`fab-dispute-preclassify --apply-dir recovery-s208/out` auto-resolved **49/72** of the
non-excluded rows (48 AUTO_CLEAR + 1 AUTO_DISPUTED), leaving **23 NEEDS_READ** edges — all
action-verb edges (IMPRISONS/CAPTURES/BETRAYS/EXECUTES/APPOINTS/RESCUES/DEPOSES/…) whose
edge_type isn't in the flat-genealogy AUTO_CLEAR whitelist.

## Adjudication (23 NEEDS_READ, primary-text-anchored per S200/S202)

Read each row's chapter passage (`sources/chapters/fab/<unit>.md`). **20 confirmed** as flat
canon where the chronicler hedge was proximity noise; **3 dropped**:

1. **`CAPTURES corlys→alicent`** — the quote ties Alicent's seizure to men "who had worn the
   seahorse badge of House Velaryon," but at the Judgment of the Wolf those captors are tried
   as individual opportunists (gutter-knights Perkin had dubbed), condemned/spared on their own.
   The text gives Corlys no agency. Dropped as house-badge→house-lord over-attribution.
2. **`RULES tyland→seven-kingdoms`** — quote is "gathered more and more power to himself" while
   the regency council "convened less and less often." That's informal power-accretion by the
   Hand under a regency, not sovereignty. `RULES <realm>` is a monarch relation. Dropped.
3. **`SAME_AS nettles→netty`** — "Netty" is a diminutive used for the same girl in the same
   passage, not a separate identity. Per the alias-not-SAME_AS convention (Reek/Alayne), a
   nickname belongs in `aliases:`, not a cross-identity edge. Dropped; queued "Netty" as a
   `nettles` alias to the harvest queue.

None needed a tier-2 `disputed` tag — confirming the false-positive hypothesis. Verdicts were
generated programmatically from the actual rows (exact string matches) into
`verdicts-s209-disputes.jsonl`, with the 3 drops keyed by (edge_type, source, target) tuple.

## Two landing subtleties that mattered

This was a **re-merge**, not a fresh apply — S208 had already minted+merged each unit's
non-dispute rows. Two traps had to be dodged:

**Edges.** Each recovery `candidates.json` still carries the S208 run_id, which is already in
`edges.jsonl` → mint's re-run guard would abort. Fix: bump each unit's `_meta.run_id` to
`…-recovery-disputes-s209`. Mint's edge-level same-quote dedup (step 3.5) then skipped every
already-landed S208 edge and appended only the 44 new `DISP*` edges. Verified `edges.jsonl`
grew +44 / −0. (The `via: dispute-inject` marker stays in candidates.json only — mint ignores
unknown keys by design, so it isn't propagated to edges.jsonl.)

**Prose.** fab_merge_node keys its skip on a run_id-specific marker. Re-running under the
*old* run_id → `skipped_marker` (the new bullets never land). Re-running under a *fresh*
run_id on the *augmented* merge-plan → the block would contain the S208 bullets **plus** the
new ones → duplicated S208 bullets. Fix: build a **dispute-only** merge-plan by diffing each
unit's post-inject merge-plan against a pre-inject snapshot, keeping only the added lines.
First cut produced one entry per (unit, slug); the dry-run exposed a second trap — several
slugs (corlys-velaryon, eustace, orwyle, nettles, …) appear across multiple units, so multiple
entries shared one run_id and all-but-the-first would hit `skipped_marker`. **Consolidated to
one entry per slug** (11 slugs / 24 bullets) → fab_merge_node `section_extended` each node with
a single fresh block. Zero duplicate bullets (verified with `uniq -d`).

## The EXCLUDED_UNITS false-positive

`fab-heirs-of-the-dragon-15-p01` (1 row) and `-p02` (3 rows) collide **by name** with the
S200-smoke `EXCLUDED_UNITS` guard hard-coded into both preclassify and inject. That guard
protects the *standard* `apply/` dir's already-adjudicated S200 data; here in
`recovery-s208/out/` these same-named dirs hold **fresh, unlanded** S208 recovery rows — so the
guard is a false-positive that would silently drop 4 of the 76. Ran preclassify+inject on just
those two units with the guard patched off (a scratchpad runner that importlib-loads the real
modules, sets `EXCLUDED_UNITS = frozenset()`, scopes via `--units`, and calls `main()` —
reusing 100% of the deterministic logic; `chapter=unit` provenance preserved). All 4 were flat
AUTO_CLEAR. This is a latent script bug: the guard should be conditional on the apply-dir, not
an unconditional name match — noted for whoever next reuses dispute-inject on a non-standard dir.

## Gates & totals

- `fab-semantic-gate` → OVERALL PASS, 4/4 (0 new VICTIM_IN and 0 disputed *edges*, so the
  harm-gate and disputed-invariant were trivially satisfied).
- `pytest` 1457 passed · `deno task test` (web/) 100 passed.
- No `weirwood refresh`: prose-append edits node bodies only (no new slugs/aliases/nodes), so
  `graph/index/` stays valid (S205 quote-only precedent). Avoided the timestamp-churn/revert dance.
- `edges.jsonl` **26,308 → 26,352** (+44). 11 character nodes gained a dispute FAB block (+24
  bullets). Event nodes unchanged (1,242). 5 events deferred; 3 edges dropped.

**Disposition of all 76:** 68 landed (44 edges + 24 prose) · 3 dropped (logged) · 5 events
deferred (out of dispute-inject scope by policy, logged to `dispute-events-deferred.jsonl`).

## Endsession housekeeping

- Fixed a pre-existing bug in `history/worklog-archives/archive042.md`: the S203 entry was
  present **twice** (byte-identical duplicate from an earlier endsession). Deduped, then
  archived S204 into it (now S202–S204), fixed the stale header.
- Continue prompt `2026-07-10-recovery-dispute-drain.md` archived; the review-bucket track is
  fully closed. No single next track is fired — it's Matt's pick, with the **edge-vocab
  retrofit (Part B)** the top open graph track.
