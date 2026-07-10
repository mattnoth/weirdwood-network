# SESSION 204 — F&B causal spine (wire the new Targaryen-history event layer)
> **This is Session 204.** Stamp your worklog entry `### Session 204` at endsession.
> **Recommended model:** **Fable/Opus** orchestrator (causal typing is judgment-heavy — which
> beat CAUSES vs TRIGGERS vs MOTIVATES is exactly the class the arc-enrichment machine used
> full-strength models for) + Haiku fresh-verify (A/B-proven S202) for excerpt checks.
> **PRE-REQ:** S203 committed+pushed (harvest drained, 30 deferred events minted). If
> `git log` disagrees with worklog.md S203, STOP and reconcile.

## Why (Matt-sequenced 2026-07-09, S203)
The F&B layer now has ~993 event nodes and 1,938 book-fab role edges, but almost NO causal
wiring — the S203 live probe showed `walk_chain(death-of-queen-rhaenyra)` returns EMPTY.
Show-watchers ask "why did X happen"; the chat's walk_chain panel is bare for the whole
Dance. Matt's ordering: **causal spine (this session) → cross-era seams (next: Blackfyre,
Dark Sister, Dragonstone, dragon-skulls, and CONSIDER D&E which has no Pass 1) → edge-vocab
retrofit (backlog)**.

## Inputs (all staged)
1. **`working/fire-and-blood/causal-spine-seeds-s203.jsonl`** — 53 harvest rows of kind
   causal-spine, each a located chain sketch (e.g. "Moon's assassination → host disintegrates
   → way to Oldtown clear → Jaehaerys crowned"; fields: row, snippet, note, unit, line —
   line=0 means wrap-span, grep the unit).
2. **`working/fire-and-blood/apply/zero-edge-stubs-s203.jsonl`** — 38 zero-edge F&B event
   stubs + 3 no-home future-mint candidates at the foot. Wiring these IS part of the spine
   work (a stub with no edges can't join a chain). Absorbs B1's dropped PART_OF re-adds
   (murmison, aegon-uncrowned-seizes).
3. The Dance arc itself: the ~90 S201–S203 minted Dance/aftermath events (grep
   `pass_origin: pass-fab-enrichment` + era) — the marquee chains are Dance-internal
   (Viserys names Rhaenyra heir → greens form → usurpation → Blood&Cheese → … → death of
   Aegon II → regency).

## The task
1. **Deterministic prep first** (`feedback_python_before_agent`): build the candidate list —
   parse the 53 seeds into ordered beat-pairs; list all fab-era event nodes with their
   occurred/sort_keys years; propose candidate PRECEDES pairs from years alone (deterministic,
   no LLM). Output a work manifest.
2. **Causal typing** (the judgment step): for each seed chain + each marquee Dance sequence,
   emit CAUSES / TRIGGERS / MOTIVATES / ENABLES / PART_OF edges **with a verbatim quote per
   edge** (mint validates quotes — curly-quote/wrap gotchas: copy EXACTLY from source;
   `authoritative_line` joins wrapped lines). Use the locked vocabulary only. Chain-as-arc
   rules apply (S105/S106: NO umbrella parents; agency-collapse check; see memory
   `project_narrative_arc_reification`).
3. **Fresh-verify** each proposed causal edge vs primary text (Haiku, orchestrator re-verifies
   flagged rows — the S200 pattern: subagent verdicts get spot-checked, 2 of 4 clears were
   once wrong).
4. **Mint** via a hand-built candidates pack + `scripts/mint_enrichment.py` (S203 example:
   `working/fire-and-blood/apply/fab-deferred-events-s203/candidates.json`). Then
   `weirwood refresh` → `scripts/fab-semantic-gate.py --baseline-orphans 67` →
   `scripts/test-fab-reconcile.py` + pytest + (if goldens shift) repin ONLY after
   root-causing (S203 precedent: prominence-driven family.json shift was legitimate;
   mustInclude is the invariant).
5. **Verify the payoff live-shaped:** `weirwood query --causal-chain death-of-queen-rhaenyra`
   (and 2–3 other marquee Dance events) must return a real chain. Deploy is Matt-gated —
   offer it.

## Success criteria
- walk_chain non-empty for the marquee Dance events (death-of-queen-rhaenyra, death-of-aegon-ii,
  blood-and-cheese-ish beats, storming-of-the-dragonpit, battle-of-the-gullet).
- ≤ a handful of zero-edge fab stubs remain (each remaining one justified in the report).
- Every new edge quote-grounded; gate PASS; all suites green.

## DO NOT
- Do NOT re-run extraction. Do NOT start cross-era seams (NEXT session), theories, or the
  strip track (Matt-gated). Do NOT auto-run /endsession (needs Matt's go).
- Do NOT mint umbrella parent nodes for chains (S105/S106 chain-as-arc rule).
- Do NOT trust year-only PRECEDES pairs as causal edges — PRECEDES is temporal, causal types
  need textual grounding.
