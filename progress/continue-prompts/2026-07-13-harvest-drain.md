# SESSION — Harvest drain 37→0 (parallel-safe secondary; runs in any window)

> **Session number:** take the next free S-number at YOUR endsession (this is the
> secondary track; the theories mint-gate session is the primary and may claim S217
> first — check worklog.md before stamping).
> **Recommended model:** **Sonnet** orchestrator + 2 disjoint-dir Sonnet attachers +
> a Haiku fresh-verify sample. Cheapest-viable; no Fable needed.
> **Parallel-safe:** touches ONLY `graph/nodes/` quote sections + `working/harvest-queue.md`
> — no edges.jsonl, no `working/theories/`, no chat code.

## State

`working/harvest-queue.md` has **37 open rows**, all origin-tagged S216:
- 30 rows auto-merged from cluster PROPOSAL.md HARVEST sections — **RAW/UNNORMALIZED**
  (bullet text copied into the note column by a mechanical parser; kind column
  defaulted to "quote"; some cites use ranges or `file.md.NNN` forms). Normalize as
  you triage.
- 7 rows hand-merged from verifier/agent final messages (clean).

## The work (the S152/S205/S215 machine)

1. Triage each row: line-check the cite against `sources/chapters/` (correct drift;
   the S216 pressure-test row batch had 2 drifts caught at merge), fix kind labels,
   resolve target node (existing only — rows needing a mint get `parked` with reason).
2. Route rows → disjoint node-dirs → up to 2 parallel Sonnet attachers (byte-copied
   quotes into `## Quotes` / description fields; dedup against existing content).
3. `python3 scripts/verify_node_quotes.py` → must PASS for every attach; fix fails
   by re-byte-copy.
4. Haiku fresh-verify a ~25% sample (entity-fit).
5. Flip rows `done`/`parked`; record counts in your worklog entry.
6. NOTE: a quote-only drain SKIPS `weirwood refresh` (S205 process note — avoids
   8k+ timestamp churn); no index rebuild needed for quote attaches.

## DO NOT

- Do NOT touch `working/theories/` (staged mint-gate artifacts — another session owns them).
- Do NOT mint nodes (park instead). Do NOT touch edges.jsonl. Do NOT deploy.
- Do NOT run /endsession without permission.

Vocabulary: Pass = big numbered corpus sweep; Track = named chunk of work; step
(lowercase) = ordered piece inside a Track; Tier = confidence rating 1–5 ONLY.
