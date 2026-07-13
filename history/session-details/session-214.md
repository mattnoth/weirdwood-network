---
session: 214
date: 2026-07-13
track: graph (Theories track, wave 1)
model: Fable 5 orchestrator + Sonnet extractors/proposer + Haiku residue-grounders/fresh-verifiers
graph_mutation: NO (everything staged in working/theories/; one accidental dry-run node write reverted same minute)
---

# Session 214 — Theories wave 1: the full ASX pipeline ran; R+L=J cluster staged at the mint gate

## What this session was

The first execution session of the Theories track (gate opened S213). The continue
prompt's plan — extraction → re-grounding → first builds — ran end-to-end across all
15 wave-1 Alt Shift X videos, and the R+L=J cluster (the prompt's designated first
unit) went the full dip machine: propose → adversarial fresh-verify → orchestrator
adjudication → quotecheck → dry-run mint. Matt then directed **all theory nodes stay
on staging** pending thoughtful validation — so wave 1 ends with zero graph mutation
and a validated, byte-verified staging corpus.

## Pipeline built (three deterministic scripts + two agent specs)

1. `scripts/theories-vtt-clean.py` — VTT → plain text (all 15 uploaded-caption files).
2. `scripts/theories-reground.py` — the deterministic matcher, adapted from the S213
   quote-cite upgrader: exact normalized containment (threshold lowered to 12 chars —
   uniqueness is the filter for short ASX fragments) + a trimmed-token-window layer
   (≥8 tokens/40 chars) for caption drift. Corpus = all 410 chapter files incl. D&E
   + F&B.
3. `scripts/theories-reground-repair.py` — the trust-nothing post-pass over agent
   output: re-locates every "grounded" quote (strict norm, then a loose
   quote-mark-stripped layer for nested-quotation style clashes), repairs line
   numbers, relocates cross-file, flips liars to `byte-fail`. Rescues previously
   failed rows on re-run.
4. `working/theories/extraction-spec.md` + `working/theories/regrounding-agent-spec.md`
   — the per-agent contracts (schema, spoken-quote discipline, harvest rule, honesty
   rules).

## Numbers

- 15/15 transcripts extracted (Sonnet, ~1 agent/video): **21 theory headers, 792
  beats, 244 spoken quotes**. Multi-theory videos handled (Rhaegar video split R+L=J
  vs Rhaegar-as-Azor-Ahai; Bloodraven video yielded 5 headers; Hooded Man 2).
- Deterministic re-grounding: **110 matched** / 50 ambiguous / 68 no-match / 430
  needs-agent / 134 not-groundable (show/community/GRRM/TWOW — fenced by design).
- Haiku residue grounding (≈16 agents incl. splits + redos): **296 grounded and
  byte-verified** after repair; 222 honest ungrounded; 36 byte-fails excluded.
- **Total byte-verified verbatim cites: 406.**

## Incidents

1. **Monthly spend limit + power outage** mid-fleet: ~10 agents died, several AFTER
   writing their outputs (salvaged); Bloodraven extraction + the first proposer
   launch lost and cleanly re-run next day. Incremental-file-per-agent design meant
   zero rework beyond relaunches.
2. **Haiku quote hallucination, caught mechanically**: one GNC residue agent quoted
   from memory — all 14 of its rows byte-failed (e.g. an invented "Catelyn had never
   liked this bastard…" line that exists nowhere). A stern-reprompt redo grounded
   6/14; the S213 "deterministic byte-check outranks agent verdicts" rule is now
   structural in this track (repair pass runs on every agent file).
3. **`mint_enrichment.py` validation-mode gap**: `--edges/--backup` pointed at
   scratch still wrote the NEW NODE file into the real `graph/nodes/theories/`.
   Deleted within the same minute; live edges.jsonl untouched (26,740). Fix queued
   (todos): a `--nodes-root` override.

## R+L=J cluster — the staged first unit

- **New node `r-plus-l-equals-j`** (tier-3, `status: show-confirmed` with explicit
  show≠canon note) + **enriched `knight-of-the-laughing-tree-theories`** stub
  (tier-2→3, `status: open`) — both in `working/theories/rlj-cluster/`, NOT minted.
- **13 edges** (12 SUPPORTS / 1 CONTRADICTS), every quote byte-copied from chapters.
- Fresh-verify (2 Haiku adversaries): 12C/2A/0R. Adjudications: **T8 dropped to
  premise prose** (Robert's official abduction account is what the theory re-argues —
  neither SUPPORTS nor CONTRADICTS); **T9 requoted** to the crowning's own line;
  **T6 downgraded tier-3→tier-4** (House-of-the-Undying blue flower = stacked
  vision-symbolism) — first use of intra-theory edge-tier variance.
- Gates: quotecheck 13/13; slug pre-check 10+1; dry-run mint green on scratch copy.
- Record: `working/theories/rlj-cluster/ADJUDICATION-s214.md`.

## Design decisions taken (Matt to ratify at the staging review)

- One node per canonical named theory; wiki "X/Theories" umbrella stubs stay dark.
- SUPPORTS/CONTRADICTS = evidence-node → theory-node, each edge carrying its own
  byte-verified quote; theory-layer edges tier 3–5, variance allowed per edge.
- CITED_BY deferred — no out-of-world source node type exists (ASX/Poor Quentyn
  aren't `object.text`); provenance lives in frontmatter `video_sources` + `origin`.
- `claim:` belongs in frontmatter (proposer had it body-only; fixed at adjudication).
- Ungrounded material lives in a domain-labelled node section, never edges.

## Matt directives this session

- Usage limit reset confirmed; "not worried about Sonnet/Haiku subagents."
- **"The real X" ASX character epics endorsed → front of the wave-2 queue** (README updated).
- **All theory nodes stay on STAGING** — thoughtful validation/testing before any mint;
  next session discusses schema + integration and the next theory builds.
