# Advisory Board Review — narrative-arc containers (Essos + WO5K)
**Date:** 2026-06-21 (S120 follow-on) · **Method:** 4 parallel read-only Sonnet subagents, distinct lenses (structure/hierarchy · causal-semantics/drift · process/methodology · taxonomy/boundaries). Casual fresh-eyes audit requested by Matt.

## Headline: all 4 = ON TRACK, yes-with-caveats.
The chain-as-arc / no-umbrella model, the reification role-vocab, and especially the **sequence-only-trap discipline** (refusing CAUSES on campaign battle-sequences) were praised by every lens as the system's crown jewel. No restructure needed. Caveats are additive: a query-tool gap, two missing containers, and small process hardening.

## Convergent findings (ranked by leverage)

1. **ENABLES traversal gap [raised independently by lens 1 AND lens 2 — highest signal].** `graph-query.py --causal-chain` walks only `{CAUSES,TRIGGERS,MOTIVATES}`. The Essos spine has 4 `ENABLES` hinges (drogo-vow→ritual; astapor→yunkai→meereen; wedding→daznak), so the "AGOT→ADWD spine" is actually **3 disconnected segments** in the primary query tool — and `--causal-chain fall-of-astapor` returns 0/0 despite live ENABLES edges. The *semantic* choice (ENABLES≠CAUSES) is correct; the *tooling* shouldn't make the spine invisible. **Fix:** add `--include-enables` / `--full-chain` flag (label ENABLES hops as preconditions). ~5–10 lines. Affects every ENABLES edge in both containers.

2. **Two missing containers [lens 4].** ~half the dark foreshadowed events have no container home: (a) **NORTH/Wall** — Jon's assassination (#21), LC election (#16), Stannis→Winterfell (#24), Manderly/Grand-Northern-Conspiracy (#27); (b) **AEGON / Targaryen-restoration** — Varys/Illyrio tunnel conspiracy (AGOT, Arya witnesses) → Aegon's landing (#23) → Varys kills Kevan (#25). The Essos E7 dyad belongs to this AEGON thread, not Essos. **Fix:** name both as scopes in the backlog now (no dip required yet) so dark events have a home.

3. **Cross-container seam [lens 4].** `robert-orders-daenerys-assassination` is double-membership (WO5K downstream + Essos upstream) but is labeled "standalone prime mover," which hides that it's the *join* between the two biggest containers. **Fix (doc-only, no graph change):** annotate it as a cross-container bridge in both decomp docs.

4. **E7/E8 are wrong-shape (dyads, not causal arcs) [lens 2 + 4].** They'll always be deferred as Essos junctures. **Fix:** extract them into a "dyad queue" (relationship-enrichment), not the arc backlog.

5. **Container retrieval as it grows [lens 1].** Doc-only container is right for authoring but weak for retrieval. **Fix (optional, pairs with #1):** a `container:` frontmatter tag + `--container <name>` query mode — cheap, avoids the umbrella-parent anti-pattern the team correctly rejected.

6. **Process hardening [lens 3]:** (a) add a **slug-existence pre-check** to the mint-script template (catches the `daznak-s-pit` vs `daznaks-pit` dedup-miss class before edges land); (b) add "re-read the line and confirm before appending" to the harvest snippet (3 queue cites had drift this session); (c) formalize **verified-at-mint vs independent-fresh-verify** as two gate levels (Level 2 = independent, required for cross-book/contested CAUSES).

7. **One edge to reconsider [lens 2]:** `sons-of-the-harpy-kill-twenty-nine TRIGGERS wedding-of-hizdahr` (S119 E2) — mild agency-collapse (Dany's multi-week deliberation); TRIGGERS may be too strong → consider CAUSES, or split into `MOTIVATES daenerys` + `daenerys CAUSES wedding`. Minor; flag. (Also: Rhaego's death is reachable only via `SACRIFICES`, not the causal walk — minor.)

## What every lens said NOT to change
The fresh-verify-at-mint adjudication (catching CAUSES→ENABLES downgrades, the Rhaegal-not-Viserion fix, the E5 two-segments call) + the decomposition-doc-as-prior-session-artifact (the real independence layer) + the sequence-only-trap rubric. Keep all three.

## Pace verdict
Lens 3: hold the current 1–2-junctures-per-session, decomp-gated tempo. Don't batch more aggressively — the decomp doc's pre-flagging of traps is what prevents the pre-S95 mass-mint failure mode.
