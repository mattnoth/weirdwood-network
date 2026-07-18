# SESSION 222 — Theories wave-2 MINT-GATE review with Matt (3 Jon Snow clusters)

> **This is Session 222.** Stamp your worklog entry `### Session 222` at endsession.
> **CHECK FIRST (rule 9):** grep `^### Session` in `worklog.md` — S220/S221 were claimed by the S219-era parallel windows (theory-toggle, and one more per Matt); if 222 is also taken, take the next free number and note it.
> **Recommended model: Fable** — mint-gate adjudication with Matt (wave-1 precedent, S218).
> **This is a GRAPH-MUTATING session if Matt says go — never run alongside another graph-mutating window.**

## What this session is

Matt reviews the staged wave-2 theory clusters and decides: mint all / some / none. The S218 go covered wave 1 only. Everything below is BUILT, VERIFIED, and DRY-RUN GREEN — the only missing input is his go.

## The staged tally (S219)

**28 edges (27 SUPPORTS / 1 CONTRADICTS; tiers all in the 3–5 floor) + 1 new node + 1 enriched stub**, staging dirs under `working/theories/jonsnow-cluster/`:

1. **resurrection/** — 16 edges: 13 → NEW `jon-snow-resurrection` (concept.theory; second-life-in-Ghost / Melisandre-revival-at-cost / transformation) + 3 → existing `azor-ahai-theories` (JR14/15 SUPPORTS, JR16 CONTRADICTS). Verifiers 32/32 CONFIRM, both NODE PASS. Z7/Z8/Z9 dedup clean. Node file: `resurrection/nodes/jon-snow-resurrection.node.md`.
2. **enrich/** — 9 edges: 6 → `r-plus-l-equals-j` (Bael parallel, crypt dreams, baby-swap echo t3, Howland-witness t3, Ned's-evasiveness, Aemon parallel) + 3 t5 → `bloodravens-grand-plan` (steering-catalogue beats, mechanism-assumed notes). 2 dropped at adjudication (JE1 factual mismatch, JE2 irony-not-evidence).
3. **nightsking/** — 3 edges → `nights-king-theories` stub ENRICHED (`nightsking/enrich/nights-king-theories.node.md` replaces the live stub at mint time) + **claim-style display rename "Jon Snow may become a new Night's King"** (KotLT precedent — **Matt ratifies or reverts the rename**). NK2 carries the adjudicated Stark-Lord-Commander-precedent reading.

Records: `working/theories/jonsnow-cluster/{resurrection,enrich,nightsking}/ADJUDICATION-s219.md` (read all three before the review — they carry the verifier splits + orchestrator rulings Matt may want to interrogate).

## Open questions for Matt (walk these in order)

1. Mint all 3 clusters / subset / none?
2. Ratify the nights-king-theories claim-style display rename? (Old title kept as alias either way.)
3. The resurrection cluster includes 2 proposer-found extra-substrate edges (JR1 subject-link, JR8) that passed quotecheck + both verifiers — OK as precedent, or does he want proposer-additions pre-flagged differently in future waves?
4. 13 residual byte-fail beats (post-redo) — declare terminal (park) or queue one more targeted redo?

## Mint procedure on go (per cluster)

1. `python3 scripts/mint_enrichment.py --candidates working/theories/jonsnow-cluster/<c>/candidates.json` (LIVE — no overrides; per-cluster backups land in `graph/edges/_regrounding/`).
2. resurrection: mint writes `graph/nodes/theories/jon-snow-resurrection.node.md` from its nodes/ dir. nightsking: after the edge mint, copy `nightsking/enrich/nights-king-theories.node.md` over the live stub (the wave-1 enrich-apply pattern).
3. Gates after ALL minted clusters: `bash scripts/weirwood-refresh.sh` (new node → alias/index rebuild is REQUIRED) · `python3 scripts/verify_node_quotes.py` · pytest · deno task test · tier-floor spot-audit on the new edges.
4. Worklog + todos + memory (`project_theories_track_deferred`) updates; archive this prompt.

## Vocabulary (paste into any subagent prompts — they don't load CLAUDE.md)

Pass = big numbered corpus sweep; Track = named chunk of work; step (lowercase) = ordered piece inside a Track; Tier = confidence rating 1–5 ONLY.

## DO NOT

- Do NOT mint without Matt's explicit per-cluster go in THIS session (staging survives fine if he holds).
- Do NOT touch the chat SHARED_RULES guardrail (toggle build owns it).
- Do NOT deploy (Matt-gated; next deploy ships the theory layer to dossiers regardless).
- Do NOT re-run proposers/verifiers — the validation is done; this is a review-and-mint session.
- Do NOT run /endsession without permission.
