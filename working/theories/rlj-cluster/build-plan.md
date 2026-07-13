# R+L=J cluster — build plan (S214, theories wave 1, first unit)

> Orchestrator design decisions for the first theory build. The proposer agent
> executes against this; fresh-verify + adjudication + dry-run follow. NO MINT
> without Matt's explicit go (the S213 autonomous grant was session-scoped).

## Inputs

- Extractions: `working/theories/extractions/{kHqzFwodZqQ,UrhqmMRv1gQ,eUVr_lUxYf8}.jsonl`
- Deterministic grounding: `working/theories/regrounding/<id>.jsonl` (status `matched`)
- Agent grounding: `working/theories/regrounding-agent/<id>.jsonl` (status `grounded`)

## Node decisions (orchestrator, S214)

1. **Mint NEW `r-plus-l-equals-j`** (`concept.theory`, → `graph/nodes/theories/`).
   - `confidence: tier-3` (strongest textual case in the fandom; Tier 3–5 ALWAYS for theories)
   - `status: show-confirmed` (the show revealed Jon's parentage; show ≠ book canon — status only annotates)
   - `origin: "ASOIAF fan community (pre-1997 Usenet era; canonical statement via fan analyses)"`
   - `video_sources`: kHqzFwodZqQ + UrhqmMRv1gQ (R+L=J beats only)
   - aliases: "R+L=J", "R plus L equals J", "Jon Snow parentage theory", "Rhaegar and Lyanna theory"
   - Body: `## Claim`, `## Evidence For` (grounded beats w/ verbatim quote + cite),
     `## Evidence Against`, `## Status Notes` (show outcome, ASX verdict).
2. **Enrich EXISTING `knight-of-the-laughing-tree-theories`** (dark wiki stub, slug kept).
   - claim: the mystery knight at the tourney at Harrenhal was Lyanna Stark
   - `confidence: tier-3`, `status: show-confirmed`? NO — the show never confirmed KotLT → `status: open`.
   - video_sources: eUVr_lUxYf8. Sub-variant candidates (Howland, Bran-warg) stay body prose.
3. **`jon-snow-theories` umbrella stub stays dark** (wiki-page artifact; no clean edge type to a member theory — flag for Matt).
4. **Rhaegar-as-Azor-Ahai beats from UrhqmMRv1gQ are HELD** for the Azor Ahai unit (extraction in flight) — no double-mint.

## Edge decisions

- `SUPPORTS` / `CONTRADICTS`: **existing evidence node → theory node**, one edge per
  grounded beat family (dedupe: several beats often share one evidence node — merge
  into one edge with the strongest quote; extra quotes go to the theory node body).
- Every edge carries a **grounded verbatim quote + chapter cite** (mint fail-fast re-greps).
- **Edge tier = the theory node's tier (tier-3)** — the evidence LINK is interpretive
  even when the quoted passage is Tier-1 canon. Standing-decision candidate for Matt.
- `CITED_BY` (theory → theorist/video) **DEFERRED**: no out-of-world source node type
  exists (`object.text` = in-world texts). Provenance lives in frontmatter
  `video_sources` + `origin`. Design question for Matt (same class as the open
  title-node question).
- Evidence-node candidates (pre-mint dedup: these EXIST): `combat-at-the-tower-of-joy`,
  `tourney-at-harrenhal`, `crowning-of-lyanna-at-harrenhal`, `abduction-of-lyanna`,
  `roberts-rebellion`, characters `eddard-stark`, `lyanna-stark`, `rhaegar-targaryen`,
  `jon-snow`, `daenerys-targaryen` (House of the Undying vision). Proposer verifies
  slugs via graph/nodes/ lookup before emitting; NO new evidence-node mints in this
  unit unless a marquee beat has no home (flag, don't mint).

## Guardrails (hard)

- Theory claims NEVER enter tier-1/2 or other nodes' prose as fact.
- Chat surface untouched (SHARED_RULES no-theories guardrail stays).
- Ungrounded beats (show/TWOW/community/grrm + honest UNGROUNDED) may appear in the
  theory node body ONLY under an explicitly-labelled "Ungrounded / outside the corpus"
  subsection with their domain named — never as edges.
- Stop after dry-run; Matt's go gates the mint.
