# SESSION 202 — F&B bulk reconcile-apply: BATCHES 4–7 (the Dance of the Dragons)
> **This is Session 202.** Stamp your worklog entry `### Session 202` at endsession.
> **Recommended model:** **Fable** (or Opus) — per-unit judgment: CREATE fresh-verify + dispute
> adjudication with PRIMARY-TEXT verification. These batches hold ALL 62 dispute rows; S200 proved
> 2 of 4 subagent clears were wrong, so the orchestrator must re-verify tags against the text.
> **PRE-REQ:** batches 1–3 are APPLIED + committed (`57a825d1fe` is B3). Sweep tooling P1–P7 is built
> + committed. If `git log` doesn't show the B1–B3 commits, STOP and reconcile with worklog.md.

## State (S201 close — trust worklog.md over this, CLAUDE.md rule 9)
The advisory-board pre-mint sweep (P1–P7) is DONE + committed. S200 residue cleaned. Global dispute
auto-inject applied (66 edges + 155 prose). **Batches 1–3 (15 units, sec 04–14, all pre-Dance) APPLIED**
(book-fab edges 264→847). Live state + full batch table: `working/fire-and-blood/apply/BATCH-PROGRESS-s201.md`.
Sweep record: `working/fire-and-blood/apply/SWEEP-s201.md` + `GATE-s201.md`.

## The task — apply batches 4–7 (the Dance), same S200 §8 rhythm
Batches (chronological; ~5 units each, one git commit per batch):
- **Batch 4** (14–16, Dance opens): long-reign-cont-14-p03, 14-p04, heirs-15-p03, blacks-greens-16-p01, 16-p02
- **Batch 5** (17, Dance war): red-dragon-17-p01, p02, p03, p04 — also sanity-check the one char CREATE "Aegon (nephew of Maegor)" in 17-p01
- **Batch 6** (18–21, Dance end): rhaenyra-18-p01, p02, short-sad-19, hour-of-wolf-20, hooded-hand-21
- **Batch 7** (22–25, aftermath+appendix): war-peace-22-p01, p02, voyage-alyn-23, lysene-24-p01, p02, lineages-25

Per unit / per batch:
1. **CREATE fresh-verify** (fresh subagent, batch-level): dupe/rename/parent vs the graph. Feed the batch's
   CREATE inventory + apply-dir nodes/. Reuse the batch-1/2/3 prompt shape (see session-201 detail).
2. **Dispute adjudication** — the batch's NEEDS_READ + ROMANCE_CLASS rows (from each unit's
   `dispute-preclass.jsonl`; AUTO_CLEAR/AUTO_DISPUTED were already injected). Fresh subagent verdicts BUT
   **you re-verify each tag against ±10 lines of the chapter yourself** (S200 lesson). Watch the
   "eustace"/"mushroom" false-positive class (a chronicler name that is also a CHARACTER's given name — S201
   B3 "Eustace Hightower" was one). Patterns: euphemistic "favorite" LOVER_OF = disputed/unattributed; flat
   "paramour" = tier-1; exile-decree divergence = gyldayn-synthesis. "Secret marriage of Rhaenyra & Daemon"
   (heirs-15-p03) is the marquee genuinely-contested beat.
3. **Surgery** — `python3 scratchpad/fab-apply-surgery.py --spec <spec.json> [--apply]` (FOLD + RENAME,
   auto-locates unit). For ADD_PARENT: a PART_OF edge NEEDS a locatable verbatim quote (reuse the child's
   role-edge quote from candidates.json; DROP if none). Verdicts: `python3 scripts/fab-dispute-inject.py
   --unit <u> --policy auto --verdicts <verdicts.jsonl>` (verdict schema {unit,kind,source,target,edge_type,
   verdict:clear|disputed|drop[,in_universe_source]}).
4. **Apply per unit:** git checkpoint → `python3 scripts/mint_enrichment.py --candidates .../candidates.json`
   → `python3 scripts/fab_merge_node.py --merge-plan .../merge-plan.json` (MUST show 0 skipped / 0 not-found).
5. **After each batch:** `weirwood refresh` → `python3 scripts/fab-semantic-gate.py --baseline-orphans 67`
   (must be OVERALL PASS) → `python3 scripts/test-fab-reconcile.py` (153 green) → commit.

NOTE: orphan junk .node.md files were already cleaned across all 35 units (S201) — batches 4–7 won't hit
that. Query-engine CLI: `PYTHONPATH=graph/query python3 -m weirwood_query.cli resolve "<name>"` (the old
`scripts/graph-query.py` is a shim).

## Close-out (after the LAST unit, batch 7, applies)
- Deterministic Lineages-appendix validation diff (design §3.4/§10.10) → contradictions triage.
- Review-bucket triage plan (present a summary, not row-by-row).
- **F&B harvest-queue drain** (`working/fire-and-blood/harvest-fire-and-blood.jsonl` — 315 rows; + main queue).
- **Deferred-events triage** (37 rows in each unit's `dispute-events-deferred.jsonl` — decide create-node-or-skip).
- The 2 PART_OF dropped in B1 (murmison, aegon-uncrowned-seizes — no locatable quote) + the sun-chaser B3
  borderline fold: optional re-visit.
- Un-park check: the strip-boilerplate track un-parks ONLY after the last pack applies (todos.md ★CURRENT).
- Residue sweeps: `vaegon`/`vaegon-targaryen` dupe; `great-council-of-101-ac` mistype; chat-bundle rebuild rides next deploy.

## DO NOT
- Do NOT re-run extraction (row-level quarantine exists) or touch the extraction prompt.
- Do NOT skip per-unit CREATE fresh-verify or dispute adjudication, or the per-batch semantic gate.
- Do NOT mint a PART_OF without a locatable verbatim quote. Do NOT touch the parked strip track.
- Do NOT auto-run /endsession.
